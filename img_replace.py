import os
import zipfile
import shutil
import time
from github import Github
from PIL import Image
import re
import os
from github import Github

# Step 1: Unzip files
for file in os.listdir('.'):
    if file.endswith('.zip'):
        with zipfile.ZipFile(os.path.join('.', file), 'r') as zip_ref:
            zip_ref.extractall('unzipped')

# Step 2: Compress images
md_files = []
for root, dirs, files in os.walk('unzipped'):
    for file in files:
        if file.endswith('.md'):
            md_files.append(file)
        elif file.endswith('.png'):
            img = Image.open(os.path.join(root, file))
            # img.save(os.path.join(root, file), optimize=True, quality=10)
            img = img.convert("RGB")  # Convert to RGB
            img.save(os.path.join(root, file.replace('.png', '.jpg')), "JPEG", optimize=True, quality=20)

# Step 3: Move images to new directory
if md_files:
    blog_name = re.findall(r'(.*) \w+\.md', md_files[0])
    if blog_name:
        blog_name = blog_name[0]
    else:
        blog_name = 'unknown'
else:
    blog_name = 'unknown'
new_dir = './' + blog_name + '_' + str(int(time.time()))
os.makedirs(new_dir)
for root, dirs, files in os.walk('unzipped'):
    for file in files:
        if file.endswith('.jpg'):
            shutil.move(os.path.join(root, file), new_dir)

# Step 4: Create PR and upload directory (you need to replace 'your_token', 'your_repo', 'your_branch' with your actual values)
g = Github('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')
repo = g.get_repo('blog-imgs')
repo.create_git_ref(ref='refs/heads/' + 'master', sha=repo.get_commits()[0].sha)

# Upload all files in the directory
for root, dirs, files in os.walk(new_dir):
    for file in files:
        with open(os.path.join(root, file), 'rb') as f:
            content = f.read()
            repo.create_file(os.path.join(root, file), 'upload imgs of {}'.format(new_dir), content, branch='master')

# # Step 5: Replace image links in md files
# for root, dirs, files in os.walk('unzipped'):
#     for file in files:
#         if file.endswith('.md'):
#             with open(os.path.join(root, file), 'r+') as f:
#                 content = f.read()
#                 content = content.replace('![Untitled]', 'your_image_url')
#                 f.seek(0)
#                 f.write(content)
#                 f.truncate()