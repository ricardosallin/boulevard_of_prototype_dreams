# 🗺️ LLM na Unha

**Resumo:**  
Sallin queria começar a entender os LLM's e foi perguntar pro GPT. A conversa foi relativamente longa e gerou um experimento em Excel pra ver as contas que formam uma rede neural funcionando ao vivo.
Conforme: 
- conceitos e exercicio com 1 neurônio! https://chatgpt.com/c/67eafc1b-6518-800d-997c-6940a68a7194
- detalhando as derivadas envolvidas: https://chatgpt.com/c/67f7118c-07d8-800d-96d5-268f1b3e2173
- novo experimento de rede neural com 2 neurônios: https://chatgpt.com/c/6812e472-7538-800d-89e6-94b59981821a

---

## 🧠 Motivação

> "Mas como funciona tudo isso? Será q dá pra ir no mais baixo nível de tudo?"

---

## 🔁 Fluxo do raciocínio

|Pergunta|Resposta|
|--------|--------|
| 1. Sallin começou perguntando sobre os "parâmetros" e escalas de tamanho (na época o GPT ainda divulgava essa info)  | GPT: <br>- modelos como o GPT estão na casa do trilhão. Modelos com milhões de parâmetros ainda podem ser úteis em contextos muito específicos |
| 2. Sallin perguntou sobre a forma física desses parâmetros: um grande "CSV" ou banco de dados? | GPT: - matrizes multidimensionais números reais<br>- formatos físicos: .h5 (HDFS) ou .pt (PyTorch)<br>- 1 milhão de parâmetros poderia ser uma matriz 1000 x 1000 |
| 3. Sallin: como criar LLM's para ler bases de dados? | GPT: totalmente possível com embedding+RAG ou outras abordagens |


Nesta altura o Sallin começou a pensar mais hipoteticamente (aka pirar na batata) em modelos muito pequenos :)


|Pergunta|Resposta|
|--------|--------|
| 4. Sallin: o que daria pra fazer com modelos de 10, 100, 1 mil parâmetros? | GPT: equações polinomiais, distinguir com dificuldade números escritos à mão (base do MNIST), detectar sujeito/verbo/objeto em frases simples, reconhecer padrões em imagens pequenas. A partir do milhão já dá pra criar frases simples |
| 5. Sallin começou a entender! Redes neurais são ineficientes, mas com a escala surgem **NOVAS CAPACIDADES** | GPT: É exatamente isso! Ineficiência, mas com escala vêm aprendizado de padrões adaptabilidade com generalização |
| 6. Sallin: e o consumo computacional? | GPT <br>- treinamento: bilhões de operações de multiplicação de matrizes multidimensionais (backpropagation), muitas CPUs rodando por dias ou meses, gastando muita energia<br>- inferência (responder perguntas): é apenas o Forward Pass, bem menor, mas ainda consome<br>- Em Watts: busca no google 0,3 W / consulta ao GPT ~10-50 W / treinar um LLM gigante Gigawatts! |


Aqui começou a parte sangrenta de código! Criar um nano-modelo


|Pergunta|Resposta|
|--------|--------|
| 7. Sallin resolveu criar um modelo pequeno de 16 parâmetros | GPT gerou o código PyTorch para criar uma rede de 8+8 neurônios para aprender a função `y = 2a + 3b + 5`|
| 8. Sallin conseguiu rodar o código, perguntou sobre a saída: Loss baixando exponencialmente a cada época, pesos e vieses de cada camada, etc | GPT confirmou cada item com detalhes |
| 9. Sallin pediu mais detalhes sobre como os pesos e vieses chegam na função objetivo `y = 2a + 3b + 5` | GPT: o modelo vai tentando várias combinações, tendo como base apenas pares de entrada e saída, até chegar aos parâmetros, o que (em geral) costuma acontecer com bastante precisão. (esses pares de entrada e saída eram os parâmetros A, B e a saída Y da própria função objetivo! Um exemplo clássico de aprendizado supervisionado. Mas isso ainda não estava claro para o Sallin) |
| 10. Sallin seguiu acompanhando as contas, pediu em planilhas, e neste momento quis entrar na caixa-preta e entender as contas "na unha" | GPT explicou o Forward Pass, o cálculo do erro com MSE (erro quadrático médio) e por fim a "mágica" do Backpropagation envolvendo gradientes descendentes para atualizar os pesos, e a repetição disso em épocas. Propôs um exemplo mais simples com 1 entrada e 1 neurônio |
| 11. Sallin pediu esse exemplo mais simples | GPT: função objetivo: y=2x+1<br>- entrada X = 3<br>- saída Y = 7<br>- inicializando o neurônio com W = 0,5 (peso) e B = 0,0 (viés), com Learning Rate (LR) = 0,1 <br>- calculou o Forward Pass: ^y = 1,5<br>- calculou o erro (MSE): 30,25<br>- determinou os gradientes do backpropagation (derivadas) <br>- atualizou o peso pra W = 3,8 e viés pra B = 1,1<br>- e isso foi a época 1!  |
| 12. Sallin amou essa descida ao fundo do mar! Pediu a próxima época | GPT repetiu Forward Pass (12,5), Loss (30,25)e Backpropagation<br>- e atualizou novamente W = 0,5 e B = 0,0<br>- voltou ao ponto anterior! Modelo oscilando entre extremos, não vai sair do lugar<br>- propôs baixar o Learning rate, adicionar mais exemplos ou só ver a oscilação acontecendo  |
| 13. Sallin escolheu baixar o Learning Rate | GPT baixou o LR = 0,01 <br>- refez FP, BP e atualizou pra W = 1,094 e B = 0,198 |
| 14. Sallin pediu mais algumas épocas | GPT seguiu em frente!<br>- época 3: W = 1,3052, B = 0,2684<br>- época 4: W = 1,4742, B = 0,3247 <br>- época 5: W = 1,6094, B = 0,3698 <br>- erro a essa altura baixou de ~30 para apenas ~5: **o modelo está aprendendo!** |
| 15. Sallin pediu mais algumas épocas | GPT seguiu com os cálculos<br>- Na época 10: W = 1,9729 (chegando perto de 2) e viés B = 0,4909, e o erro caiu para apenas ~0,5<br>- Na época 15: W = 2,0919, B = 0,5306, Loss = 0,0584 |
| 16. Sallin pediu mais épocas pra ver, mas entendeu que os ganhos são decrescentes. Perguntou o que acontece se, nesta altura, mudarmos a entrada de (3,7) para outra coisa | GPT: o modelo simplesmente vai usar a informação atual (W = 2,0919, B = 0,5306) com a nova entrada. <br>- **Isso é a inferência (ou predição)! Rodar apenas o Forward Pass com uma nova entrada**<br>- E podemos seguir com mais épocas (cálculo do Loss e backpropagation) para ele continuar adaptando o peso e viés |
| 17. Sallin finalmente entendeu! O modelo **não sabe** que o peso tem q ser 2 e o viés tem q ser 1. Ele **chega sozinho** nisso, apenas fazendo essas contas com o input!! | GPT deu graças aos céus: até que enfim!! kkk<br>- Propôs dar 4 pares de exemplo em vez de apenas 1 (aumentar o contexto) |
| 18. Sallin pediu essa alteração! (a essa altura já estava com um Excel em paralelo e acompanhando todas essas contas na unha!) | GPT refez o exemplo, agora voltando ao PyTorch: modelo com 1 neurônio e 4 inputs no tensor <br>- Mas o sallin continuou fazendo lá no Excel. Na prática o q muda é só no cálculo do Loss/MSE, que agora é pela média dos 4 Forward Passes com os inputs<br>- deu certinho! W = 1,99 e B = 1,02, com Loss de apenas 0,0017. O modelo aprendeu! |
| 19. Sallin tentou em paralelo com o código, mexeu nos inputs, colocou escalas de números diferentes, e viu o modelo "alucinando" ao vivaço | GPT: impacto de valores desbalanceados para estabilidade numérica <br>- modelo tenta capturar tudo, mas com 1 neurônio é mais difícil: "uma só reta pra encaixar tudo"<br>- Solução A: baixar learning rate pra 0.0001<br>- Solução B: normalizar os dados: (x - média) / desvpad<br>- Solução C: usar técnicas de regularização ou otimizadores (Adam, etc) |
| 20. Sallin testou todas as abordagens: todas funcionaram | GPT: <br>- "Se os dados têm escalas diferentes, normaliza!"<br>- "Se o modelo tá instável, pisa no freio!"<br>- "Otimizadores modernos = mágicos do século XXI"<br>- propôs novos passos! Regularização, camadas de ativação linear e não-linear, batches de treinamento, dados ruidosos  |

---

## 🤖 Conclusão

- GPT deu um panorama geral de como funcionam os LLM's
- Dissecou os detalhes sangrentos das contas necessárias: Forward Pass, Loss, Backpropagation e atualização de pesos/vieses
- Simulou diversas situações da vida nervosa das redes: explosão do Loss, learning rate alto demais, dados não normalizados, etc
- Gerou exemplo de código com PyTorch, mas produziu (indiretamente) uma "rede neural em Excel"!
- e o Sallin foi dormir 4h da manhã :)

---

## 🧭 Próximos passos

- 🔁 Batchs de treinamento (mini-batches) — que ajudam em datasets grandes
- 🎯 Regularização (L2, Dropout) — pra evitar overfitting
- 🧪 Brincar com dados ruidosos / não-lineares (e ver o modelo falhar!)
- 🧠 Adicionar camadas e ativação não-linear (pra sair do domínio linear)

---

## 📝 Notas finais

**É POSSÍVEL fazer Data Science no Excel!** (pelo menos experimentos didáticos -- porque sim, a didática importa)

---

## 🧠 Leia a conversa completa

> [conceitos e exercicio com 1 neurônio!](https://chatgpt.com/c/67eafc1b-6518-800d-997c-6940a68a7194)
> [detalhando as derivadas envolvidas](https://chatgpt.com/c/67f7118c-07d8-800d-96d5-268f1b3e2173)
> [novo experimento de rede neural com 2 neurônios](https://chatgpt.com/c/6812e472-7538-800d-89e6-94b59981821a)


> 📁 Ou leia a transcrição arquivada em: [`conversa.md`](./conversa.md)

