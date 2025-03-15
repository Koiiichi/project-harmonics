import mido
from mido import MidiFile, MidiTrack, Message

# Function to map particle IDs to MIDI note numbers
def map_id_to_note(particle_id):
   id_to_note = {
       -11: 60,  # Positron
       211: 62,  # Pion
       321: 64,  # Kaon
       2212: 67,  # Proton
   }
   return id_to_note.get(particle_id, 60)  # Default to positron note

# Function to map momentum to MIDI velocity
def map_momentum_to_velocity(momentum):
   # You can adjust this mapping to suit your needs
   return int((momentum - 0.2) / (5.2 - 0.2) * 127)

# Function to map theta to MIDI pitch bend within the valid range
def map_theta_to_pitch_bend(theta):
   # Calculate the pitch bend value within the valid MIDI range
   bend_value = int((theta - 0.55) / (1.5 - 0.55) * 16383) - 8192
   # Ensure the value is within the valid range
   return max(min(bend_value, 8191), -8192)

# Load your CSV data and create a MIDI file
csv_file = "yourfilename.csv" #Add the path of your CSV file
midi_file = MidiFile()
track = MidiTrack()
midi_file.tracks.append(track)

# Define a grace period (in MIDI ticks) when transitioning between notes
grace_period = 300  # Adjust the duration as needed

with open(csv_file, 'r') as file:
   # Skip the header line
   next(file)
   
   previous_id = None  # To keep track of the previous particle ID
   for line in file:
       id, p, theta = map(float, line.strip().split(','))
       note = map_id_to_note(id)
       velocity = map_momentum_to_velocity(p)
       pitch_bend = map_theta_to_pitch_bend(theta)


       # Add a note-on event
       track.append(Message('note_on', note=note, velocity=velocity))


       # Check if there's a previous ID and it's different from the current ID
       if previous_id is not None and previous_id != id:
           # Add a grace period (pause) before transitioning to the new note
           track.append(Message('control_change', control=64, value=0,
                                time=grace_period))  # Control change 64 is the Sustain Pedal


       # Add pitch bend event
       track.append(Message('pitchwheel', pitch=pitch_bend))


       # Add a note-off event after a short duration (adjust as needed)
       track.append(Message('note_off', note=note, velocity=0, time=700))


       previous_id = id  # Update the previous ID for the next iteration


# Save the MIDI file
midi_file.save("Addyourfilename.midi") # You would need a blank midi file before you can save the code. Link a blank MIDI file you have or anyone downloaded from the internet. 
