import os
import zipfile
import sys

if __name__ == '__main__':
    zip_file = zipfile.ZipFile(os.path.join('dist', f'timechart_{sys.platform}.zip'), 'w', zipfile.ZIP_DEFLATED)

    dist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "timechart")

    print(f"Dist path: {dist_path}")

    for root, dirs, files in os.walk(dist_path):
        for file in files:
            zip_file_name = os.path.relpath(os.path.join(root, file), os.path.join(dist_path, '..'))
            print(f"Adding {zip_file_name} to zip")
            zip_file.write(os.path.join(root, file),
                           arcname=zip_file_name)

    zip_file.close()
