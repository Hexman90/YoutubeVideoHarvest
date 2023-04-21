import os
import csv
from project import write_channels_to_file, get_channels_id, get_existing_channels

# Tested just 3 of the functions that read/write to a file
# For the other functions since involves user or api interraction, it's harder to test.


def test_get_existing_channels(tmpdir):
    # Create a temporary csv file with test data
    channels_csv = tmpdir.join("channels.csv")
    channels_csv.write("Title,ID\nChannel1,12345\nChannel2,23456\n")

    # Change the current working directory to the tmpdir
    os.chdir(tmpdir)

    # Call the function and assert the result
    existing_channels = get_existing_channels()
    assert existing_channels == ["Channel1", "Channel2"]


def test_write_channels_to_file(tmpdir):
    # Create a temporary csv file with test data
    channels_csv = tmpdir.join("channels.csv")
    channels_csv.write("Title,ID\nChannel1,12345\n")

    # Change the current working directory to the tmpdir
    os.chdir(tmpdir)

    channels_id_title = {"Channel2": "23456", "Channel3": "34567"}
    existing_channels = ["Channel1"]

    write_channels_to_file(channels_id_title, existing_channels)

    # Read the updated csv file and assert the result
    with open("channels.csv", newline='') as file:
        reader = csv.DictReader(file)
        channels = [row for row in reader]
        
    assert channels == [{"Title": "Channel1", "ID": "12345"},
                        {"Title": "Channel2", "ID": "23456"},
                        {"Title": "Channel3", "ID": "34567"}]



def test_get_channels_id(tmpdir):
    # Create a temporary csv file with test data
    channels_csv = tmpdir.join("channels.csv")
    channels_csv.write("Title,ID\nChannel1,12345\nChannel2,23456\n")

    # Change the current working directory to the tmpdir
    os.chdir(tmpdir)

    # Call the function and assert the result
    channel_ids = get_channels_id()
    assert channel_ids == ["12345", "23456"]

