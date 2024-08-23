from baselanguage import BaseLanguage
from exceptions import CodeException, PrintException
import subprocess
import os
import re

class JuliaLanguage(BaseLanguage):
    def __init__(self, langExtension:str): 
        self.__offsetCodeLines = 1
        self.__baseCodeLines = -1
        super().__init__(langExtension)
    
    def base_code_with_args(self, baseCode: str, name_file_professor: str, funcName: str, funcNameProf: str, arg, returnType = ""):
        #print(f"baseCodeLines: {self.__baseCodeLines}")
        self.__baseCodeLines = len(baseCode.splitlines())
        importProfLine = f'include("{name_file_professor}.jl")\n'
        codesComparisonOutput = f"\nprintln({funcName}({arg}...) == {funcNameProf}({arg}...))\nprintln({funcName}({arg}...))\nprintln({funcNameProf}({arg}...))"
        resultArgs = importProfLine + baseCode + codesComparisonOutput
        return resultArgs
    
    def professor_code_with_args(self, professorCode: str, funcName: str, funcNameProf: str, arg, returnType = ""):
        baseProfCode = professorCode.replace(funcName, funcNameProf)  #Trocando o nome da função no arquivo do professor
        outputProf = f"\nprintln({funcNameProf}({arg}...))"   #Servirá para printar o output da solução correta
        outputProfCode = baseProfCode + outputProf
        return baseProfCode, outputProfCode
    
    def evaluate_file(self, absolute_path: str):    #Por enquanto, não há verificações para Julia
        return
    
    def run_code(self, file_path: str, isProfessorCode: bool):
        result = subprocess.run(["julia", file_path], capture_output=True, text=True)
        if result.stderr != "":
            error_message = process_errors(result.stderr, self.__offsetCodeLines, self.__baseCodeLines, file_path)
            raise CodeException(error_message)
        outputs = result.stdout.split("\n")
        if isProfessorCode:
            return outputs[0]
        outputs[0] = True if outputs[0].upper() == "TRUE" else False
        return outputs
    
    def run_pre_process_code(self, file_path: str):
        return
    
    def pre_process_code(self, code: str, code_path: str):
        code_without_comments = re.sub(r'#=(.*?)=#', '', code, flags=re.DOTALL)
        code_without_comments = re.sub(r'#.*$', '', code_without_comments, flags=re.MULTILINE)
        code_without_comments = code_without_comments.strip()
        print_regex = re.compile(r'\b(print|println)\s*\(.*\)|@\b(printf|show)\b')
        has_print = bool(print_regex.search(code_without_comments))
        if has_print:
            raise PrintException("")
        self.run_pre_process_code(code_path)
        return code_without_comments
    
    
def process_errors(stderr: str, offSetLines: int, baseCodeLines: int, file_path: str):
    path = os.path.normpath(file_path)
    result_path = os.sep.join(path.split(os.sep)[-3:])  #Pegando os 3 últimos diretórios do caminho relativo do arquivo
    result_path_without_file_name = os.sep.join(path.split(os.sep)[-3:-1])
    
    match_undef_var = re.search(r"ERROR: LoadError: UndefVarError: `(.+?)` not defined.*?:(\d+)", stderr, re.DOTALL) #Regex para capturar erro de variável indefinida
    other_errors = re.compile(r'ERROR:\s+([\w]+):\s+([\w\s.-]+):\s+(.*)')
    other_errors_match = other_errors.search(stderr)
    
    error_type = ""
    error_message = ""
    line_number = -1
    
    if match_undef_var:
        var_name = match_undef_var.group(1)
        error_message = f"ERROR: LoadError: UndefVarError: `{var_name}` not defined"
    elif other_errors_match:
        error_type1 = other_errors_match.group(1).strip()
        error_type2 = other_errors_match.group(2).strip()
        error_type = error_type1 + ": " + error_type2
        error_message = other_errors_match.group(3).strip()
        if result_path_without_file_name in error_message:
            error_parts = error_message.split('"')
            file_name = ""
            full_path = ""
            for error_part in error_parts:
                if result_path_without_file_name in error_part:
                    full_path = error_part
                    last_slash_index = max(error_part.rfind('/'), error_part.rfind('\\'))
                    file_name = error_part[last_slash_index + 1:]
                    file_name = file_name.split(":")[0]
                    break
            if file_name != "":
                error_message = error_message.replace(full_path, file_name)
            else:
                error_message = ""
        error_message = f"{error_type}: {error_message}"
        if "Expected `end`" in stderr:
            error_message += " - Expected `end`"
    
    #Procurando a linha:
    stacktrace_pattern = re.compile(r'@\s*(.*\.jl):(\d+)')
    stacktrace_matches = stacktrace_pattern.findall(stderr)
    if stacktrace_matches:
        for file_name, line in stacktrace_matches:
            if result_path in file_name:
                line_number = int(line.strip()) - offSetLines
                break
    if baseCodeLines != -1 and line_number != -1:
        if int(line_number) <= baseCodeLines:
            error_message += f" on line {line_number}"
    return error_message