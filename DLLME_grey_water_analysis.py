import os
from plot_funcs import open_pda, plot_pda


dir_path = r"path/to/data"
save_dir_path = r"path/to/data"

dir_list = os.listdir(dir_path)  # get name of files in directory
print(*[element + "\n" for element in dir_list])

for file_name in dir_list:
    print("\nREADING " + file_name)

    # Extract PDA data
    PDA_data, wavelength, time = open_pda(os.path.join(dir_path, file_name))

    # Plot PDA contourf
    plot_pda(
        PDA_data,
        time,
        wavelength,
        x_min=0,  # min retention time
        # x_max=5,    # max retention time
        y_min=200,  # min wavelength
        y_max=400,  # max wavelength
        z_min=-5000,  # min intesity
        z_max=50000,  # max intesity
        lvls=30,  # levels of the counter plot
        save_path=os.path.join(save_dir_path, file_name + ".png"),
    )
