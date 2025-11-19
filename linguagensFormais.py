import re

# Validador de CPF
def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(cpf.split())  # Remove espaços e caracteres não numéricos
    if len(cpf) != 11 or not cpf.isdigit():
        return False  # CPF deve ter exatamente 11 números

    # Verificando se todos os números são iguais (casos como '111.111.111-11' devem ser rejeitados)
    if cpf == cpf[0] * len(cpf):
        return False

    # Calculando os dois dígitos verificadores
    def calcular_dv(cpf, pesos):
        soma = sum(int(cpf[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Pesos para os dois cálculos de dígitos verificadores
    pesos_1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    # Calculando os dígitos verificadores
    dv_1 = calcular_dv(cpf, pesos_1)
    dv_2 = calcular_dv(cpf, pesos_2)

    return cpf[-2:] == f'{dv_1}{dv_2}'  # Comparando os dois últimos dígitos com os calculados

# Validador de E-mail (utilizando expressão regular)
def validar_email(email: str) -> bool:
    # Expressão regular para validação de e-mails
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(regex, email) is not None

# Classe para o Autômato Finito Determinístico (DFA) para validação de CPF e E-mail
class DFAValidator:
    def __init__(self):
        # Estados e transições para o DFA
        self.states = {'start', 'email_valid', 'cpf_valid', 'invalid'}
        self.start_state = 'start'
        self.accept_states = {'email_valid', 'cpf_valid'}
        self.transitions = {
            'start': {'email': 'email_valid', 'cpf': 'cpf_valid'},
            'email_valid': {'email': 'invalid', 'cpf': 'invalid'},
            'cpf_valid': {'email': 'invalid', 'cpf': 'invalid'},
            'invalid': {'email': 'invalid', 'cpf': 'invalid'},
        }

    def validate(self, input_value: str, input_type: str):
        if input_type == 'email':
            if not validar_email(input_value):
                return False
            else:
                return True
        elif input_type == 'cpf':
            if not validar_cpf(input_value):
                return False
            else:
                return True
        else:
            return False  # Tipo de entrada inválido

# Teste do validador de e-mails e CPF
def test_validators():
    dfa = DFAValidator()

    # Testando E-mails
    emails = [
        "teste@dominio.com",    # Válido
        "invalid_email@.com",    # Inválido
        "outro@dominio.br",      # Válido
        "erro@dominio..com"      # Inválido
    ]

    print("Resultados para validação de e-mail:")
    for email in emails:
        result = dfa.validate(email, 'email')
        print(f"E-mail: {email} - {'Válido' if result else 'Inválido'}")

    # Testando CPFs
    cpfs = [
        "123.456.789-09",    # Inválido
        "111.111.111-11",    # Inválido
        "222.444.666-25",    # Válido
        "000.000.000-00"     # Inválido
    ]

    print("\nResultados para validação de CPF:")
    for cpf in cpfs:
        result = dfa.validate(cpf, 'cpf')
        print(f"CPF: {cpf} - {'Válido' if result else 'Inválido'}")

if __name__ == "__main__":
    test_validators()
