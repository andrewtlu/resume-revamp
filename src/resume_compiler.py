import subprocess


def compile_latex(input_file, compiler="lualatex"):
    try:
        # Run the LuaLaTeX compiler
        subprocess.run([compiler, input_file], check=True)
        print(f"Compilation successful: {input_file} has been compiled to PDF.")
    except subprocess.CalledProcessError:
        print(f"Error: Compilation failed for {input_file}.")


# Replace 'document.tex' with your LaTeX file name
# if __name__ == '__main__':
#     latex_file = '../dat/resume_template/bba_resume_template.tex'
#     compile_latex(latex_file)
