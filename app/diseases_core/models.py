from django.db import models


class DiseaseType(models.Model):
    code = models.CharField(max_length=12, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Disease Types"
        verbose_name = "Disease Type"
        ordering = ["-pk"]

    def __str__(self) -> str:
        return f"{self.code}: {self.short_name}"

    def save(self, *args, **kwargs) -> None:
        self.code = f"{self.code}".lower()
        self.short_name = f"{self.short_name}".lower()
        return super().save(*args, **kwargs)


class Disease(models.Model):
    disease_type = models.ForeignKey(
        "diseases_core.DiseaseType", null=True, blank=True, on_delete=models.CASCADE
    )
    code = models.CharField(max_length=12, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    specific_gender = models.CharField(max_length=1, null=True, blank=None)
    umls_id = models.CharField(max_length=10, null=True, blank=True)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Diseases"
        verbose_name = "Disease"
        ordering = ["-pk"]

    def __str__(self) -> str:
        return f"{self.disease_type}: {self.short_name}"

    def save(self, *args, **kwargs) -> None:
        self.code = f"{self.code}".lower()
        self.short_name = f"{self.short_name}".lower()
        self.disease_type = f"{self.disease_type}".lower()
        self.specific_gender = f"{self.specific_gender}".lower()
        return super().save(*args, **kwargs)
