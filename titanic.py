import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Titanic interactive Museum",layout="wide") #configuración de la página


@st.cache_data #Stores cache

def load_data(): #function to load data
    df = pd.read_csv(r'C:\Users\leo21\Desktop\Upgrade_hub\Github_projects\Titanic_project\Titanic_project\titanic.csv') 
    df_clean = df.copy()
    return df_clean



data = load_data() 

data['Survived'] = data['Survived'].map({0: 'Dead', 1: 'Alive'})
st.sidebar.image(r"C:\Users\leo21\Desktop\Upgrade_hub\Github_projects\Titanic_project\Titanic_project\Pictures\tema-ilustracion-iceberg.png", width=150)
option = st.sidebar.radio( #Creates a radio button on the sidebar
    "Select a section:",
    ["Landing", "Passengers distribution by ticket","Passengers class distribution","Passengers port distribution", "See Dataset"]
)

st.sidebar.header("Filters") #create a header


def load_all(lista): #function to add 'All' to a list
    return ["All"] + list(lista)



def apply_filters(df_clean, filters): #function to apply filters
    for col, val in filters.items():
        if val != ['All']:
            if not val:
                val = df_clean[col].unique() .tolist()
            elif df_clean[col].dtype in [np.int64, np.int32]:
                val = list(map(int, val))
            elif df_clean[col].dtype in [np.float64, np.float32]:
                val = list(map(float, val))
            df_clean = df_clean[df_clean[col].isin(val)]
        
    return df_clean



st.title("Titanic Database")

def show_landing(): #function to show landing section
    st.header("Welcome to the Titanic Museum Database")
    st.write("Use the side menu to navigate through different sections and obtain specific information.")
    st.image(r'C:\Users\leo21\Desktop\Upgrade_hub\Github_projects\Titanic_project\Titanic_project\Pictures\k-mitch-hodge-y-9-X5-4-vU-unsplash.jpg', caption = 'Credits: K. Mitch Hodge via Unsplash')

    with st.expander('Data origin'):
        st.markdown("""
                    The data used in this project has been provided by Upgrade Hub. This dataset has 891 rows and 12 columns, where our variables are:
                       - **PassengerId**: Unique number for each passenger.
                       - **Survived**: Whether passengers survived or not.
                       - **Pclass**: In which class passengers traveled.
                       - **Name**: First and last name, as well as title if they have one.
                       - **Sex**: Gender.
                       - **Age**: Age.
                       - **SibSp**: If passengers have siblins or spouses traveling with them.
                       - **Parch**: If passengers have parents or children traveling with them.
                       - **Ticket**: Ticket number.
                       - **Fare**: Ticket price.
                       - **Cabin**: Cabin number.
                       - **Embarked**: Acronym of the embarkation port.
                       
                       I have cleaned almost 20% of null/NaN data in the 'Age' column, 77% in the 'Cabin' column and 0.2% in the 'Embarked' column.
                       The columns I used the most are: Survived, Pclass, Name, Sex, Ticket and Embarked.
                       """)
    
    with st.expander("History of RMS Titanic"):
        st.write("The RMS Titanic was the largest passenger ship in the world at the end of its construction, which sank in the Atlantic in 1912 after colliding with an iceberg. In the sinking, 1,496 people of the 2,208 on board died. Here we find data on some of those passengers.")

    with st.expander("Route map"):
        st.write("The titanic picked up passengers in Southampton(S), Cherbourg(C) and Queenstown(Q)-(The city of Queenstown is currently called Cobh)-. The number of passengers picked up at each port is shown here.")
        st.image(r'C:\Users\leo21\Desktop\Upgrade_hub\Github_projects\Titanic_project\Titanic_project\Pictures\AdobeStock_322554404.jpeg', caption='Adobe Stock')
        port_counts = data['Embarked'].value_counts()
        fig = px.pie(port_counts, values=port_counts.values, names=port_counts.index, title='Total passengers per port')
        st.plotly_chart(fig)
        
    with st.expander("Conclusion"):
        st.write("Of the 891 passengers recorded in this dataset, only 342 people survived, of which 233 were women and 109 were men, making this catastrophe one of the deadliest shipwrecks in history that occurred in peacetime.")
    
def show_passengers_ticket(): #Function to show a list with ticket number and full names
    st.header("Passengers distribution by ticket")
    filters = { #dictionary with the filters we wanna use
        'Survived': st.sidebar.multiselect("Select fate:", options=load_all(data['Survived'].unique()),default=["All"]),
        'Sex': st.sidebar.multiselect("Select gender:", options=sorted(load_all(data['Sex'].unique())), default=["All"]),        
        'Embarked': st.sidebar.multiselect("Select port:", options=sorted([str(i) for i in load_all(data['Embarked'].unique())]), default=["All"])    
}
    filtered_data = apply_filters(data, filters)
    
    # Search box
    search = st.sidebar.text_input("Search by ticket number or name:", "")
    if search:
        filtered_data = filtered_data[filtered_data['Ticket'].str.contains(search) | filtered_data['Name'].str.contains(search)]
    
    fig = px.scatter(filtered_data, x="PassengerId", y="Fare", color="Fare",  size="Fare", log_x=True, size_max=50, template="plotly_dark", title="Ticket Prices", labels={"Ticket": "Ticket nº", "Fare": "Ticket fare"}, hover_data=["Ticket"])
    fig.update_xaxes(title_text="Passenger Id")
    fig.update_yaxes(title_text="Ticket fare")
    fig.update_layout(title="Fares per Ticket", title_font=dict(size=30, family="Courier", color="white"))
    st.plotly_chart(fig)
    
    
    # Group by ticket number with names
    dupli = filtered_data.groupby('Ticket')['Name'].apply(list)

    # Convert the list of names to a string
    dupli = dupli.apply(lambda x: ' / '.join(x))
    
    # Convert the groupby object to a DataFrame
    dupli_df = dupli.reset_index()

    # Rename the columns
    dupli_df.columns = ['Ticket', 'Names']

    # Display the DataFrame as an interactive table in Streamlit
    st.table(dupli_df)

def show_passengers_class(): #function to show passengers by class
    st.header("Passengers class distribution")
    filters = { #diccionario con los filtros
        'Survived': st.sidebar.multiselect("Select fate:", options=load_all(data['Survived'].unique()),default=["All"]),
        'Sex': st.sidebar.multiselect("Select gender:", options=sorted(load_all(data['Sex'].unique())), default=["All"]),        
        'Embarked': st.sidebar.multiselect("Select port:", options=sorted([str(i) for i in load_all(data['Embarked'].unique())]), default=["All"])    
}
    filtered_data = apply_filters(data, filters) #applies the filters

    fig = px.histogram(filtered_data,x='Pclass',nbins=10, title="Passengers class distribution",template='plotly_dark',color='Sex', barmode='group')
    st.plotly_chart(fig)
    
    # Add counter to optimize visualization
    total_passengers = len(data)
    total_filter = len(filtered_data)
    percentage = (total_filter / total_passengers) * 100
    st.write(f"Total passengers: {total_filter} ({percentage:.2f}% of total passengers)")

def show_passengers_port():#function to show passengers by port
    st.header("Passengers port distribution")
    filters = {
        'Survived': st.sidebar.multiselect("Select fate:", options=load_all(data['Survived'].unique()),default=["All"]),
        'Sex': st.sidebar.multiselect("Select gender:", options=sorted(load_all(data['Sex'].unique())), default=["All"])
    }
    filtered_data = apply_filters(data, filters) 
    fig = px.histogram(filtered_data,x='Embarked',nbins=10, title="Passengers Port distribution",template='plotly_dark',color='Sex', barmode='group')
    st.plotly_chart(fig)
    
        # Add counter to optimize visualization
    total_passengers = len(data)
    total_filter = len(filtered_data)
    percentage = (total_filter / total_passengers) * 100
    st.write(f"Total passengers: {total_filter} ({percentage:.2f}% of total passengers)")

def show_dataset(): #function to show the entire dataset
    st.header("Full Dataset")
    st.dataframe(data)

options = { 
    "Landing": show_landing,
    "Passengers distribution by ticket": show_passengers_ticket,
    "Passengers class distribution": show_passengers_class,
    "Passengers port distribution": show_passengers_port,
    "See Dataset": show_dataset,
}

options[option]() 
