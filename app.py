import streamlit as st
import pandas as pd

# Function to read and process the events file
def read_events(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    event_details = []
    counters = {}

    # Processing event details
    for line in lines:
        if '~' in line:
            parts = line.split(' ~ ')
            event = parts[1].strip()
            details = parts[0].strip().split(' ')
            team = details[0]
            if team.isupper() and len(team) == 3:
                player = ' '.join(details[1:-1])
                time = details[-1]
            else:
                team = ''
                player = ' '.join(details[:-1])
                time = details[-1]
            event_details.append([team, player, time, event])
        elif ':' in line:
            parts = line.strip().split(': ')
            key = parts[0].strip()
            value = int(parts[1].strip())
            counters[key] = value

    return event_details, counters

def show(events):
    # Read the events and counters
    event_details, counters = read_events(events)

    # Extract home and away team
    home_team = list(counters.keys())[0].split(' ')[-1]
    away_team = list(counters.keys())[1].split(' ')[-1]

    # Create a DataFrame for event details
    df_events = pd.DataFrame(event_details, columns=['Team', 'Player', 'Time', 'Event'])

    # Create a DataFrame for event counters
    counter_data = {
        f'{home_team}': [
            counters[f'Goals Scored by {home_team}'],
            counters[f'Yellow card {home_team}'],
            counters[f'Red card {home_team}'],
            counters[f'Substitution {home_team}']
        ],
        'Event': ['⚽ Goals Scored', '🟨 Yellow card', '🟥 Red card', '🔄 Substitution'],
        f'{away_team}': [
            counters[f'Goals Scored by {away_team}'],
            counters[f'Yellow card {away_team}'],
            counters[f'Red card {away_team}'],
            counters[f'Substitution {away_team}']
        ]
    }

    df_counters = pd.DataFrame(counter_data)

    # Create a DataFrame for total events
    total_events = {
        'Event': ['Total 🟨 Yellow card', 'Total 🟥 Red card', 'Total 🔄 Substitution'],
        'Count': [
            counters['Yellow card'] if 'Yellow card' in counters else 0,
            counters['Red card'] if 'Red card' in counters else 0,
            counters['Substitution'] if 'Substitution' in counters else 0
        ]
    }

    df_total_events = pd.DataFrame(total_events)

    # Streamlit app
    st.title('Match Events')

    # Display event details
    st.subheader('Event Details')
    df_events['Event'] = df_events['Event'].replace({
        'Goal': '⚽ Goal',
        'Yellow card': '🟨 Yellow card',
        'Red card': '🟥 Red card',
        'Substitution': '🔄 Substitution'
    })
    st.table(df_events)

    # Display event counters
    st.subheader('Event Counters')
    st.table(df_counters)

    # Display total events
    st.subheader('Total Events')
    st.table(df_total_events)

if __name__ == "__main__":
    show("events.txt")