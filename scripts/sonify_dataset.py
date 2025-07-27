import argparse
import pandas as pd
from mido import MidiFile, MidiTrack, Message

ID_TO_NOTE = {
    -11: 60,  # Positron
    211: 62,  # Pion
    321: 64,  # Kaon
    2212: 67,  # Proton
}

def map_id_to_note(particle_id):
    return ID_TO_NOTE.get(particle_id, 60)

def map_momentum_to_velocity(momentum, min_p, max_p):
    scale = (momentum - min_p) / (max_p - min_p)
    return int(max(0, min(1, scale)) * 127)

def map_theta_to_pitch_bend(theta, min_theta, max_theta):
    scale = (theta - min_theta) / (max_theta - min_theta)
    bend_value = int(max(0, min(1, scale)) * 16383) - 8192
    return max(min(bend_value, 8191), -8192)

def sonify_dataframe(df, output_midi, grace_period=300):
    midi_file = MidiFile()
    track = MidiTrack()
    midi_file.tracks.append(track)

    p_min, p_max = df['p'].min(), df['p'].max()
    theta_min, theta_max = df['theta'].min(), df['theta'].max()

    previous_id = None
    for _, row in df.iterrows():
        note = map_id_to_note(row['id'])
        velocity = map_momentum_to_velocity(row['p'], p_min, p_max)
        pitch_bend = map_theta_to_pitch_bend(row['theta'], theta_min, theta_max)

        track.append(Message('note_on', note=note, velocity=velocity))
        if previous_id is not None and previous_id != row['id']:
            track.append(Message('control_change', control=64, value=0, time=grace_period))
        track.append(Message('pitchwheel', pitch=pitch_bend))
        track.append(Message('note_off', note=note, velocity=0, time=700))
        previous_id = row['id']

    midi_file.save(output_midi)


def main():
    parser = argparse.ArgumentParser(description="Sonify particle dataset")
    parser.add_argument("csv", help="Path to processed CSV file")
    parser.add_argument("output", help="Output MIDI filename")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    sonify_dataframe(df, args.output)


if __name__ == "__main__":
    main()
