import os
import statistics

def enviar_email(destinatario, pdf_bytes):
    print(f"[SIMULADO] Enviando e-mail para: {destinatario}")
    print(f"[SIMULADO] Anexo PDF com {len(pdf_bytes)} bytes.")

def notificar_teams(score_medio):
    print(f"[SIMULADO] Notificando Teams: Score médio = {score_medio:.2f}")
