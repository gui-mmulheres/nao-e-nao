def formatar_cnpj(cnpj):
    # Remove qualquer caractere que não seja letra ou número para limpar a string
    cnpj = "".join(filter(str.isalnum, str(cnpj)))
    
    # Aplica a máscara XX.XXX.XXX/XXXX-XX
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"