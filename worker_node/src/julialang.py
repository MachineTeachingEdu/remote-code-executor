from baselanguage import BaseLanguage
from exceptions import CodeException, PrintException
import subprocess
import re

class JuliaLanguage(BaseLanguage):
    def __init__(self, langExtension:str): 
        self.__offsetCodeLines = 1
        super().__init__(langExtension)
    
    def base_code_with_args(self, baseCode: str, name_file_professor: str, funcName: str, funcNameProf: str, arg):
        importProfLine = f'include("{name_file_professor}.jl")\n'
        codesComparisonOutput = f"\nprintln({funcName}({arg}...) == {funcNameProf}({arg}...))\nprintln({funcName}({arg}...))\nprintln({funcNameProf}({arg}...))"
        resultArgs = importProfLine + baseCode + codesComparisonOutput
        return resultArgs
    
    def professor_code_with_args(self, professorCode: str, funcName: str, funcNameProf: str, arg):
        baseProfCode = professorCode.replace(funcName, funcNameProf)  #Trocando o nome da função no arquivo do professor
        outputProf = f"\nprintln({funcNameProf}({arg}...))"   #Servirá para printar o output da solução correta
        outputProfCode = baseProfCode + outputProf
        return baseProfCode, outputProfCode
    
    def evaluate_file(self, absolute_path: str):    #Por enquanto, não há verificações para Julia
        return
    
    def run_code(self, file_path: str, isProfessorCode: bool):
        result = subprocess.run(["julia", file_path], capture_output=True, text=True)
        if result.stderr != "":
            error_message = process_errors(result.stderr, self.__offsetCodeLines)
            raise CodeException(error_message)
        outputs = result.stdout.split("\n")
        if isProfessorCode:
            return outputs[0]
        outputs[0] = True if outputs[0].upper() == "TRUE" else False
        return outputs
    
    def pre_process_code(self, code: str):
        code_without_comments = re.sub(r'#=(.*?)=#', '', code, flags=re.DOTALL)
        code_without_comments = re.sub(r'#.*$', '', code_without_comments, flags=re.MULTILINE)
        code_without_comments = code_without_comments.strip()
        print_regex = re.compile(r'\b(print|println)\s*\(.*\)|@\b(printf|show)\b')
        has_print = bool(print_regex.search(code_without_comments))
        if has_print:
            raise PrintException("")
        return code_without_comments
    
    
def process_errors(stderr: str, offSetLines: int):
    error_pattern = re.compile(r'ERROR: LoadError: (.+?):\s*(.+?)\nStacktrace:\n \[\d+\] (.+?)\n\s+@ .+? (.+?):(\d+)', re.DOTALL)
    match = error_pattern.search(stderr)
    if match:
        error_type = match.group(1).strip()
        error_message = match.group(2).strip().split("\n")[0]
        if "/code" in error_message:
            error_message = ""
        function_name = match.group(3).strip()
        file_path = match.group(4).strip()
        line_number = int(match.group(5).strip()) - offSetLines
        
        error_message = f"{error_type}: {error_message}   on line {line_number}"
        return error_message
    
    return stderr
    """
    error = stderr.splitlines()[0]
    error = error.replace("ERROR: ", "")
    if error.endswith(':'):
        error = error[:-1]
    return error
    """