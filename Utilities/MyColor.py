class Colors:
    colors = {
        'BLA': '\u001b[30m',
        'RED': '\u001b[31m',
        'GRE': '\u001b[32m',
        'YEL': '\u001b[33m',
        'BLU': '\u001b[34m',
        'WHI': '\u001b[37m'
    }

    @staticmethod
    def colorful_str(**kwargs):
        return f'{Colors.colors[kwargs["color"].upper()[:3]]}{kwargs["sentence"]}{Colors.colors["WHI"]}'