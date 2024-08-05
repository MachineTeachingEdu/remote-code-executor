from baselanguage import BaseLanguage
from exceptions import CodeException, PrintException
import os
import subprocess
import json
import re

class CLanguage(BaseLanguage):
    def __init__(self, langExtension:str):
        self.__offsetCodeLines = 2
        super().__init__(langExtension)
    
    def base_code_with_args(self, baseCode: str, name_file_professor: str, funcDeclaration: str, funcDeclarationProf: str, arg):
        returnType_name = funcDeclaration.split(maxsplit=1)
        returnType = returnType_name[0].strip()
        functionName = returnType_name[1].strip()
        functionNameProf = funcDeclarationProf.split(maxsplit=1)[1].strip()
        printf_returnType = formats_printf[returnType]
        argsTxt = extract_args(arg)
        
        resultArgs = f"""#include <stdio.h>
#include "{name_file_professor}{self.langExtension}"
{baseCode}
int main() {{
    printf("%d\\n", {functionName}({argsTxt}) == {functionNameProf}({argsTxt}));
    printf("{printf_returnType}\\n", {functionName}({argsTxt}));
    printf("{printf_returnType}", {functionNameProf}({argsTxt}));
    return 0;
}}
"""
        return resultArgs
    
    def professor_code_with_args(self, professorCode: str, funcDeclaration: str, funcDeclarationProf: str, arg):
        returnType_name = funcDeclaration.split(maxsplit=1)
        returnType = returnType_name[0].strip()
        functionName = returnType_name[1].strip()
        functionNameProf = funcDeclarationProf.split(maxsplit=1)[1].strip()
        printf_returnType = formats_printf[returnType]
        argsTxt = extract_args(arg)
        
        baseProfCode = professorCode.replace(functionName, functionNameProf)   #Trocando o nome da função no arquivo do professor
        outputProfCode = f"""#include <stdio.h>
{baseProfCode}
int main(){{
    printf("{printf_returnType}", {functionNameProf}({argsTxt}));
    return 0;
}}"""
        return baseProfCode, outputProfCode
    
    def evaluate_file(self, absolute_path: str):        #Sem verificações para C
        return
    
    def run_code(self, file_path: str, isProfessorCode: bool):
        exec_file_path = compile_code(file_path, self.__offsetCodeLines)
        run_result = subprocess.run([exec_file_path], capture_output=True, text=True)
        if run_result.stderr != "":
            raise CodeException(run_result.stderr)      #todo
        outputs = run_result.stdout.split("\n")
        if isProfessorCode:
            return outputs[0]
        outputs[0] = False if outputs[0].upper() == "0" else True
        return outputs
    
    def run_pre_process_code(self, file_path: str):   #Verificando erros de sintaxe
        compile_code(file_path, 0)
    
    def pre_process_code(self, code: str, code_path: str):
        code_without_comments = re.sub(r'\/\/.*$', '', code, flags=re.MULTILINE)
        code_without_comments = re.sub(r'\/\*[\s\S]*?\*\/', '', code_without_comments, flags=re.MULTILINE)
        code_without_comments = code_without_comments.strip()
        print_regex = re.compile(r'\b(printf|puts)\s*\(.*\)')
        has_print = bool(print_regex.search(code_without_comments))
        if has_print:
            raise PrintException("")
        
        mainPart = "\nint main() {return 0;}"
        codeWithMain = code + mainPart
        with open(code_path, 'w') as file:
            file.write(codeWithMain)
        self.run_pre_process_code(code_path)   #Checando por erros na compilação do código
        return code_without_comments

formats_printf = {
    "int": "%d",
    "char": "%c",
    "float": "%f",
    "double": "%lf",
    "long": "%ld",
    "short": "%hd",
    "unsigned int": "%u",
    "unsigned char": "%c",
    "char[]": "%s",
}

def extract_args(args):
    list_args = json.loads(args)
    argsTxt = ""
    for i, arg in enumerate(list_args):
        if i == len(list_args) - 1:
            argsTxt += f"{arg}"
        else:
            argsTxt += f"{arg}, "
    return argsTxt

def compile_code(file_path: str, offSetLines: int):
    file_name_with_extension = os.path.basename(file_path)  #Nome do arquivo (com extensão)
    file_name = os.path.splitext(file_name_with_extension)[0]
    exec_file_path = file_path.replace(file_name_with_extension, file_name)
    compile_result = subprocess.run(['gcc', '-o', exec_file_path, file_path], capture_output=True, text=True)
    if compile_result.stderr != "":
        error_message = process_compile_errors(compile_result.stderr, offSetLines)
        raise CodeException(error_message)
    
    return exec_file_path

def process_compile_errors(compile_error: str, offSetLines: int):
    error_pattern = re.compile(r'([^:]+):(\d+):(\d+): (\w+): (.+)')   #Uso de expressões regulares
    function_error = ""
    error_message = ""

    for line in compile_error.splitlines():  #Percorrendo cada linha das mensagens de erro
        if " In function " in line:
            function_error = line.split("In function")[1]
            function_error = "In function" + function_error

        match = error_pattern.match(line)
        if match:
            filename, line, column, message_type, message = match.groups()
            lineNumber = int(line) - offSetLines
            error_message = f"COMPILE ERROR\n{function_error}\nLine {lineNumber}: Char {column}: {message_type}: {message}"
            return error_message
    
    return error_message