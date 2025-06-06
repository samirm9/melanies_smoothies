# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your Custom Smoothie!
  """
)

name_on_order=st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be: ', name_on_order)

# option = st.selectbox(
#     'What is your favourite fruit?',
#     ('Banana', 'Strawberries', 'Peaches'))

# st.write('Your favourite fruit is:', option)



session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'Choose upto 5 ingredients: '
    ,my_dataframe,
    max_selections =5
)


if ingredients_list:
    ingredients_string=''
    
    st.write(ingredients_list)
    st.text(ingredients_list)
    
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
        smoothiefroot_response =requests.get("https://mysmoothiefroot.com/api/fruit/watermelon")
        st_df=st.dataframe(data=smoothiefroot_response.jon(), use_container_width=True)

st.write(ingredients_string)
        
my_insert_stmt =""" insert into smoothies.public.orders(ingredients, name_on_order)
                values('""" + name_on_order + """',
                       '""" + ingredients_string + """'
                       ) """
st.write(my_insert_stmt)

time_to_insert=st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your smoothie is ordered, ' + name_on_order + '!', icon="✅")
 

