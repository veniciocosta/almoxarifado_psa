from django.db import models
from django.utils import timezone

# Create your models here.
LISTA_CATEGORIAS = (  # (armazena_no_bd, aparece_para_usuário)
    ("ACOUGUE", "Açougue"),
    ("BEBIDAS", "Bebidas"),
    ("CEREAIS", "Cereais"),
    ("COZINHA", "Cozinha"),
    ("HORTIFRUTI", "Hortifruti"),
    ("LACTICINIOS", "Lacticínios"),
    ("LIMPEZA", "Limpeza"),
    ("TEMPEROS", "Temperos"),
    ("UTENSILIOS", "Utensílios"),
)
LISTA_TIPO_MOVIMENTACAO = (  # (armazena_no_bd, aparece_para_usuário)
    ("ENTRADA", "Entrada"),
    ("SAIDA", "Saída"),
)

class Produto(models.Model):
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(max_length=50, choices=LISTA_CATEGORIAS)
    und_medida = models.CharField(max_length=255)
    quantidade = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    class Meta:
        ordering = ['descricao']

    def __str__(self):
        return self.descricao + ", " + self.und_medida

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Produto, self).save(*args, **kwargs)


class Movimentacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=50, choices=LISTA_TIPO_MOVIMENTACAO)
    quantidade = models.DecimalField(max_digits=10, decimal_places=1)
    observacao = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def __str__(self):
        return self.produto.__str__() + ", " + self.tipo + ", " + str(self.quantidade)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Movimentacao, self).save(*args, **kwargs)