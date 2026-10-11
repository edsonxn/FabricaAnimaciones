# -*- coding: utf-8 -*-
import io
p = "guion.py"
s = io.open(p, encoding="utf-8").read()
R = [
 ('"Su dueño inventó la primera criptomoneda del mundo, escribió cientos de mensajes y corrigió el código durante dos años.",',
  '"Su dueño inventó la primera criptomoneda del mundo y la cuidó durante dos años.",'),
 ('"Ese correo, revelado en un juicio en dos mil veinticuatro, es el primer rastro conocido de Satoshi Nakamoto.",',
  '"Es el primer rastro conocido de Satoshi Nakamoto.",'),
 ('        "A mediados de ese año, Satoshi empieza a entregarle el control del código a otro programador, {GA}.",\n', ''),
 ('        "Tenía el talento, la ideología, y estaba ahí desde el primer día.",\n', ''),
 ('"Un análisis de estilo encargado por la revista {FB} concluyó que su forma de escribir era la más parecida a la de Satoshi de todas las que habían comparado.",',
  '"Un análisis de estilo para la revista {FB} concluyó que su forma de escribir era la más parecida a la de Satoshi.",'),
 ('"Aun así, durante años demandó a quienes lo llamaban mentiroso, y registró a su nombre los derechos de autor del documento original.",',
  '"Aun así, durante años demandó a quienes lo llamaban mentiroso.",'),
 ('"Hasta que en dos mil veinticuatro, una alianza de empresas lo llevó a juicio en Londres para resolverlo de una vez.",',
  '"En dos mil veinticuatro, una alianza de empresas lo llevó a juicio en Londres.",'),
 ('"Reunió miles de mensajes de listas de criptografía, de mil novecientos noventa y dos a dos mil ocho, y usó inteligencia artificial para comparar cómo escribía cada participante.",',
  '"Reunió miles de mensajes de viejas listas de criptografía y usó inteligencia artificial para comparar cómo escribía cada participante.",'),
 ('"Satoshi no ponía guiones en algunas palabras compuestas, y a veces confundía dos formas parecidas del inglés. De todos los candidatos, el que más se le parecía era {BK}.",',
  '"Satoshi tenía manías al escribir, como no poner guiones en ciertas palabras compuestas. De todos los candidatos, el que más se le parecía era {BK}.",'),
 ('"{PT} lo llamó ridículo. Después contó que empezó a recibir peticiones de dinero, y que temía por su seguridad.",',
  '"{PT} lo llamó ridículo. Después contó que temía por su seguridad.",'),
 ('"En dos mil catorce, un ejercicio de estudiantes de lingüística forense en una universidad británica concluyó que su estilo era el más cercano al documento original.",',
  '"En dos mil catorce, estudiantes de lingüística forense de una universidad británica concluyeron que su estilo era el más cercano al de Satoshi.",'),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
