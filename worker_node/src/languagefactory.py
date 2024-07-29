from baselanguage import BaseLanguage
from pythonlang import PythonLanguage
from julialang import JuliaLanguage
from clang import CLanguage

class LanguageFactory():    #Aqui os objetos de linguagem serão criados
    
    @staticmethod
    def create_object_language(language_id: int) -> BaseLanguage:
        if language_id == 1:   #Python
            return PythonLanguage(".py")
        elif language_id == 2:   #Julia
            return JuliaLanguage(".jl")
        elif language_id == 3:    #C
            return CLanguage(".c")
        else:
            raise ValueError(f"Linguagem não suportada: {language_id}")