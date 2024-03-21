import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout=("wide"))

def load_data():
    try:
        data = pd.read_excel("todo_list.xlsx")
        st.success("Dados carregados com sucesso!")
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Data Inicial", "Data Final", "Tarefa", "Status", "Observação"])  # Adicionando a coluna "Observação"
        st.warning("Nenhum arquivo encontrado. Criada uma nova lista de tarefas vazia.")
    except KeyError:
        # Se a coluna "Observação" estiver ausente no arquivo Excel, adicione-a ao dataframe
        data["Observação"] = ""
        st.warning("A coluna 'Observação' não foi encontrada no arquivo. Foi adicionada uma coluna vazia.")
    return data


def save_data(data):
    data.to_excel("todo_list.xlsx", index=False)
    st.success("Dados salvos com sucesso!")

def add_task(data, new_task):
    new_task_formatted = {
        "Data Inicial": new_task["Data Inicial"].strftime("%d/%m/%Y"),
        "Data Final": new_task["Data Final"].strftime("%d/%m/%Y"),
        "Tarefa": new_task["Tarefa"],
        "Status": new_task["Status"]
    }
    new_row = pd.DataFrame([new_task_formatted])
    data = pd.concat([data, new_row], ignore_index=True)
    save_data(data)
    st.success("Tarefa adicionada com sucesso!")
    return data

def edit_task(data, index, new_data):
    data.loc[index] = new_data
    save_data(data)
    st.success("Tarefa editada com sucesso!")
    return data

def remove_task(data, index):
    data = data.drop(index)
    save_data(data)
    st.success("Tarefa removida com sucesso!")
    return data

def search_task(data, search_term):
    if data["Tarefa"].dtype == "object":
        search_results = data[data["Tarefa"].str.contains(search_term, case=False, na=False)]
    else:
        st.warning("A coluna 'Tarefa' não é do tipo string. Não é possível pesquisar.")
        search_results = pd.DataFrame()
    return search_results

def format_date(date):
    if isinstance(date, datetime.date):
        return datetime.datetime.combine(date, datetime.datetime.min.time())
    return date.strftime("%d/%m/%Y")

def main():
    st.title("Lista de Tarefas")
    data = load_data()

    action = st.sidebar.selectbox("Selecione uma ação", ["🏠 Home", "🆕 Adicionar Tarefa", "⚒️ Editar Tarefa", "⛔ Remover Tarefa", "🔍 Pesquisar Tarefa"])

    if action == "🆕 Adicionar Tarefa":
        st.subheader("Adicionar Tarefa")
        
        # Dividindo a tela em três colunas
        col1, col2, col3, col4 = st.columns(4)
    
        # Segunda coluna para o date_input da Data Inicial
        with col2:
            data_inicio = st.date_input("Data Inicial", format="DD/MM/YYYY")
    
        # Terceira coluna para o date_input da Data Final
        with col3:
            data_final = st.date_input("Data Final", format="DD/MM/YYYY")
    
        # Primeira coluna para o text_input da Tarefa
        with col1:    
            tarefa = st.text_input("Nome da Tarefa")
    
        # Quarta coluna para o radio de Status e botão de Adicionar
        with col4:
            status = st.radio("Status", ["A Fazer", "Fazendo", "Feito"])
    
            # Adicionando uma caixa de texto para inserir uma observação
            observacao = st.text_area("Observação", "")
    
            # Quando o botão "Adicionar" é clicado
            if st.button("Adicionar"):
                # Criando um dicionário com os dados da nova tarefa
                new_task = {
                    "Data Inicial": data_inicio,
                    "Data Final": data_final,
                    "Tarefa": tarefa,
                    "Status": status,
                    "Observação": observacao  # Adicionando a observação à nova tarefa
                }
                # Adicionando a nova tarefa aos dados existentes
                data = add_task(data, new_task)
            
    
        

    elif action == "⚒️ Editar Tarefa":
        st.subheader("Editar Tarefa")
        if not data.empty:
            index = st.selectbox("Selecione a tarefa para editar", data.index)
            new_data_inicio = st.date_input("Nova Data Inicial", value=pd.to_datetime(data["Data Inicial"].iloc[index], format="%d/%m/%Y"))
            new_data_final = st.date_input("Nova Data Final", value=pd.to_datetime(data["Data Final"].iloc[index], format="%d/%m/%Y"))
            new_tarefa = st.text_input("Novo Nome da Tarefa", value=data["Tarefa"].iloc[index])
            new_status = st.selectbox("Novo Status", ["A Fazer", "Fazendo", "Feito"], index=["A Fazer", "Fazendo", "Feito"].index(data["Status"].iloc[index]))
            if st.button("Salvar Edição"):
                new_data = {"Data Inicial": format_date(new_data_inicio), "Data Final": format_date(new_data_final), "Tarefa": new_tarefa, "Status": new_status}
                data = edit_task(data, index, new_data)
        else:
            st.warning("Não há tarefas para editar.")

    elif action == "⛔ Remover Tarefa":
        st.subheader("Remover Tarefa")
        if not data.empty:
            index = st.selectbox("Selecione a tarefa para remover", data.index)
            if st.button("Remover"):
                data = remove_task(data, index)
        else:
            st.warning("Não há tarefas para remover.")

    elif action == "🔍 Pesquisar Tarefa":
        st.subheader("Pesquisar Tarefa")
        search_term = st.text_input("Digite o termo de pesquisa")
        search_results = search_task(data, search_term)
        st.dataframe(search_results)

    st.dataframe(data)

if __name__ == "__main__":
    main()
