import inquirer
import matplotlib as mpl

if __name__ == "__main__":

    print("Important !: If you are using Pycharm activate 'Emulate terminal in output console' under configurations")
    confirm = {
        inquirer.Confirm('confirmed',
                         message="Do you want to view the figures instead of saving?",
                         default=True),
    }

    confirmation = inquirer.prompt(confirm)

    save = not confirmation["confirmed"]
    if save:
        mpl.use("pgf")
        mpl.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })


    from Plot import *


    label2func = {
        "Backlog vs time": figure_backlog,
        "max UEs supported vs Violation Probability": figure_3,
        "runtime vs ACB Policy": figure_runtime,
        "violation Probability vs Backlog": figure_2,
        "violation probability vs Burst resolution time": figure_5
    }

    questions = [
        inquirer.List('simulation_choice',
                      message="Which Figure do you want to create?",
                      choices=label2func.keys(),
                      ),
    ]

    answers = inquirer.prompt(questions)
    label2func[answers["simulation_choice"]](save)
