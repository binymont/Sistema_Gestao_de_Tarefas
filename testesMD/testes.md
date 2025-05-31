## Caso de Teste 1: Cadastro de Usuário

**Objetivo:**  
Verificar se o sistema permite o cadastro de novos usuários.

**Passos:**
1. Acessar a página de cadastro  
2. Preencher os campos obrigatórios (nome, email, senha)  
3. Submeter o formulário  

**Resultado Esperado:**  
Usuário cadastrado com sucesso e redirecionado para a página inicial.

**Evidência:**  
![Print Cadastro de Usuário](static/print/print1.png)

---

## Caso de Teste 2: Criação de Tarefa

**Objetivo:**  
Verificar se o sistema permite a criação de novas tarefas.

**Passos:**
1. Acessar a página inicial após login  
2. Clicar no botão "Adicionar Tarefa"  
3. Preencher os campos obrigatórios (título, descrição)  
4. Submeter o formulário  

**Resultado Esperado:**  
Nova tarefa criada e exibida na coluna "A Fazer".


**Evidência:**  
![Print Criação de Tarefa](static/print/print2.png)

---

## Caso de Teste 3: Movimentação de Tarefa

**Objetivo:**  
Verificar se o sistema permite mover tarefas entre as colunas.

**Passos:**
1. Criar uma nova tarefa  
2. Arrastar a tarefa para a coluna "Em Andamento"  
3. Arrastar a tarefa para a coluna "Concluído"  

**Resultado Esperado:**  
A tarefa é movida corretamente entre as colunas.

**Evidência:**  
![Print Movimentação de Tarefa](static/print/print3.png)

---

## Caso de Teste 4: Conclusão de Tarefa

**Objetivo:**  
Verificar se o sistema permite marcar tarefas como concluídas.

**Passos:**
1. Criar uma nova tarefa  
2. Arrastar a tarefa para a coluna "Concluído"  

**Resultado Esperado:**  
A tarefa é movida para a coluna "Concluído" e removida das outras colunas.


**Evidência:**  
![Print Conclusão de Tarefa](static/print/print3.png)

---

## Caso de Teste 5: Edição de Tarefa

**Objetivo:**  
Verificar se o sistema permite editar tarefas existentes.

**Passos:**
1. Criar uma nova tarefa  
2. Editar o título ou descrição da tarefa  
3. Salvar as alterações  

**Resultado Esperado:**  
As alterações são salvas e exibidas corretamente.


**Evidência:**  
![Print Edição de Tarefa](static/print/print5.png)

---

## Caso de Teste 6: Exclusão de Tarefa

**Objetivo:**  
Verificar se o sistema permite excluir tarefas.

**Passos:**
1. Criar uma nova tarefa  
2. Excluir a tarefa  

**Resultado Esperado:**  
A tarefa é removida do sistema.


**Evidência:**  
![Print Exclusão de Tarefa](static/print/print6.png)
