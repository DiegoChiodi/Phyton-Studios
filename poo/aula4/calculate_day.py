mes_prefix = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
dias_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

ano = int(input("Digite o ano"))
mes = -1
while(mes > 12 and mes < 1):
    mes = int(input("Digite o mes"))

dia = -1
while(dia < 1 and dia > dias_mes[mes]):
    dia = int(input("Digite o dia"))


dias_total = dia
dias_total += mes_prefix[mes - 1]
dias_total += ano * 365 + (ano % 4 == 0 and mes > 2 or (mes == 2 and dia == 29))
print(dias_total)