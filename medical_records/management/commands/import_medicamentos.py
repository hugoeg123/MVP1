import pandas as pd
from django.core.management.base import BaseCommand
from medical_records.models import MedicamentoAnvisa

class Command(BaseCommand):
    help = 'Importa medicamentos da base da ANVISA'

    def handle(self, *args, **kwargs):
        csv_path = 'DADOS_ABERTOS_MEDICAMENTOS.csv'
        
        try:
            df = pd.read_csv(csv_path, delimiter=';', encoding='latin1', usecols=[
                'NOME_PRODUTO', 
                'PRINCIPIO_ATIVO', 
                'CLASSE_TERAPEUTICA'
            ])

            for index, row in df.iterrows():
                MedicamentoAnvisa.objects.update_or_create(
                    nome_produto=row['NOME_PRODUTO'],
                    defaults={
                        'principio_ativo': row['PRINCIPIO_ATIVO'],
                        'classe_terapeutica': row['CLASSE_TERAPEUTICA']
                    }
                )
            self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo {csv_path} não encontrado. Por favor, coloque o arquivo na mesma pasta do script.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar dados: {str(e)}'))