import os
import zipfile
import sys

if __name__ == '__main__':
    platform = sys.platform

    if platform == "win32":
        platform = "win"

    if len(sys.argv) > 1:
        file_name = f'timechart_{platform}_{sys.argv[1]}.zip'
    else:
        file_name = f'timechart_{platform}.zip'

    zip_file = zipfile.ZipFile(os.path.join('dist', file_name), 'w', zipfile.ZIP_DEFLATED)

    dist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "timechart")

    print(f"Dist path: {dist_path}")

    for root, dirs, files in os.walk(dist_path):
        for file in files:
            zip_file_name = os.path.relpath(os.path.join(root, file), os.path.join(dist_path, '..'))
            print(f"Adding {zip_file_name} to zip")
            zip_file.write(os.path.join(root, file),
                           arcname=zip_file_name)

    zip_file.close()
