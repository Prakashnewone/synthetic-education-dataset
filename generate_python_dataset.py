#!/usr/bin/env python3
"""
generate_python_dataset.py

Generates three synthetic datasets and packages them into a ZIP:
1) Student/course/enrollment CSVs
2) Video courses + videos CSVs and transcripts (.txt)
3) Python modules (100 .py files) + modules_metadata.csv

Usage:
    python generate_python_dataset.py
    python generate_python_dataset.py --students 1000 --courses 100 --enrollments 5000 --video_courses 200 --videos 1000 --py_modules 100 --output education-python-datasets.zip
"""
import csv
import os
import random
import argparse
import zipfile
from datetime import datetime, timedelta

SEED = 42
random.seed(SEED)

FIRST_NAMES = ["Alex","Sam","Jordan","Taylor","Casey","Morgan","Jamie","Chris","Pat","Dana","Riley","Avery"]
LAST_NAMES = ["Smith","Johnson","Lee","Brown","Garcia","Martinez","Davis","Lopez","Wilson","Anderson","Thomas","Taylor"]
COUNTRIES = ["US","IN","GB","CA","AU","DE","FR","BR","NL","SG"]
COURSE_CATEGORIES = ["Computer Science","Mathematics","Business","Arts","Health","Language","Engineering","Data Science"]
LEVELS = ["Beginner","Intermediate","Advanced"]
VIDEO_TAGS = ["intro","tutorial","advanced","example","demo","lecture","exercise","theory"]

OUTPUT_DIR = "dataset"

def mkdirp(path):
    os.makedirs(path, exist_ok=True)

def rand_name():
    return random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES)

def rand_email(first, last):
    domains = ["example.com","mail.com","edu.org","sample.io"]
    return f"{first.lower()}.{last.lower()}{random.randint(1,999)}@{random.choice(domains)}"

def rand_text(words=8):
    pool = FIRST_NAMES + LAST_NAMES + COURSE_CATEGORIES + VIDEO_TAGS
    return " ".join(random.choice(pool) for _ in range(words))

def iso_date(days_ago=0):
    dt = datetime.utcnow() - timedelta(days=days_ago)
    return dt.strftime("%Y-%m-%d")

def generate_students(n, path):
    mkdirp(os.path.dirname(path))
    with open(path, "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["student_id","first_name","last_name","email","age","country","signup_date"])
        for i in range(1, n+1):
            sid = f"S{i:05d}"
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            email = rand_email(first, last)
            age = random.randint(16, 60)
            country = random.choices(COUNTRIES, weights=[30,20,10,8,5,5,4,4,8,6])[0]
            signup = iso_date(random.randint(0, 365*3))
            w.writerow([sid, first, last, email, age, country, signup])

def generate_courses(n, path):
    mkdirp(os.path.dirname(path))
    with open(path, "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["course_id","title","description","level","instructor_name","duration_hours","category"]) 
        for i in range(1, n+1):
            cid = f"C{i:04d}"
            title = f"Introduction to {random.choice(COURSE_CATEGORIES)} {random.randint(1,101)}"
            desc = rand_text(20)
            level = random.choice(LEVELS)
            instructor = rand_name()
            duration = round(random.uniform(1.0, 40.0), 1)
            category = random.choice(COURSE_CATEGORIES)
            w.writerow([cid, title, desc, level, instructor, duration, category])

def generate_enrollments(students_file, courses_file, n_enroll, path):
    mkdirp(os.path.dirname(path))
    students = []
    courses = []
    with open(students_file, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        students = [row['student_id'] for row in r]
    with open(courses_file, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        courses = [row['course_id'] for row in r]
    with open(path, "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["enrollment_id","student_id","course_id","enrollment_date","progress_percent","grade"])
        for i in range(1, n_enroll+1):
            eid = f"E{i:06d}"
            student = random.choice(students)
            course = random.choice(courses)
            enroll_date = iso_date(random.randint(0, 365*2))
            progress = random.randint(0,100)
            grade = random.choice(["A","B","C","D","F","Pass","Incomplete"])
            w.writerow([eid, student, course, enroll_date, progress, grade])

def generate_video_courses(n, path):
    mkdirp(os.path.dirname(path))
    with open(path, "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["video_course_id","title","category","instructor","total_duration_seconds"])
        for i in range(1, n+1):
            cid = f"VC{i:04d}"
            title = f"{random.choice(COURSE_CATEGORIES)} Series {i}"
            category = random.choice(COURSE_CATEGORIES)
            instructor = rand_name()
            total = random.randint(600, 36000)
            w.writerow([cid, title, category, instructor, total])

def generate_videos(n_videos, video_courses_file, videos_path, transcripts_dir):
    mkdirp(os.path.dirname(videos_path))
    mkdirp(transcripts_dir)
    with open(video_courses_file, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        vcourses = [row['video_course_id'] for row in r]
    with open(videos_path, "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["video_id","video_course_id","title","duration_seconds","upload_date","speaker","tags","transcript_file"])
        for i in range(1, n_videos+1):
            vid = f"V{i:06d}"
            vc = random.choice(vcourses)
            title = f"{rand_text(4).title()} Lecture {random.randint(1,50)}"
            dur = random.randint(60, 3600)
            up = iso_date(random.randint(0, 365*3))
            speaker = rand_name()
            tags = ";".join(random.sample(VIDEO_TAGS, k=random.randint(1,3)))
            tfile = os.path.join("transcripts", f"{vid}.txt")
            # write transcript
            with open(os.path.join(transcripts_dir, f"{vid}.txt"), "w", encoding='utf-8') as tf:
                tf.write(f"Title: {title}\nSpeaker: {speaker}\n\n")
                for _ in range(random.randint(3,8)):
                    sent = " ".join(rand_text(random.randint(6,12)) + "." for _ in range(random.randint(5,12)))
                    tf.write(sent + "\n\n")
            w.writerow([vid, vc, title, dur, up, speaker, tags, tfile])

# Python module generation helpers
PY_PACKAGES = ["synthetic.model", "synthetic.service", "synthetic.util", "synthetic.data"]
TYPES = ["int","float","str","bool","list","dict"]

def make_py_module(package, module_name, path):
    lines = []
    # package (as directory) is handled externally; module content:
    lines.append('"""')
    lines.append(f"{module_name} - synthetic module")
    lines.append('"""')
    lines.append("")
    imports = []
    if random.random() < 0.4:
        imports.append("from typing import List, Dict, Any")
    if random.random() < 0.2:
        imports.append("import datetime")
    for imp in imports:
        lines.append(imp)
    if imports:
        lines.append("")
    # add a simple dataclass-like class
    class_name = module_name.title().replace("_", "")
    num_fields = random.randint(1,5)
    fields = [f"field_{i}" for i in range(1, num_fields+1)]
    lines.append(f"class {class_name}:")
    lines.append("    \"\"\"Simple synthetic class\"\"\"")
    # __init__
    sig = ", ".join(f"{f}=None" for f in fields)
    lines.append(f"    def __init__(self, {sig}):")
    for f in fields:
        lines.append(f"        self.{f} = {f}")
    lines.append("")
    # simple method
    lines.append("    def to_dict(self):")
    lines.append("        return {")
    for f in fields:
        lines.append(f"            '{f}': self.{f},")
    lines.append("        }")
    lines.append("")
    # module-level functions
    num_funcs = random.randint(0,4)
    for i in range(num_funcs):
        fname = f"func_{i+1}"
        lines.append(f"def {fname}(*args, **kwargs):")
        lines.append(f"    \"\"\"Synthetic function {fname}\"\"\"")
        lines.append("    # generated placeholder logic")
        if random.random() < 0.5:
            lines.append("    return None")
        else:
            lines.append("    return {}")
        lines.append("")
    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return content, len(lines), len(imports), 1 + num_funcs  # rough method/function counts

def generate_python_modules(n, base_dir, metadata_path):
    root = os.path.join(base_dir, "python_modules")
    mkdirp(root)
    mkdirp(os.path.join(root, "__init__"))
    meta_rows = []
    for i in range(1, n+1):
        pkg = random.choice(PY_PACKAGES)
        pkg_path = os.path.join(root, *pkg.split("."))
        mkdirp(pkg_path)
        module_name = f"{random.choice(['student','course','video','utils','service','manager','record','entry'])}_{random.randint(1,999)}"
        file_path = os.path.join(pkg_path, f"{module_name}.py")
        content, lines_count, imports_count, function_est = make_py_module(pkg, module_name, file_path)
        # write __init__.py in package dirs
        cur = pkg_path
        while os.path.commonpath([root, cur]) == root:
            initf = os.path.join(cur, "__init__.py")
            if not os.path.exists(initf):
                with open(initf, "w", encoding="utf-8") as f:
                    f.write("# package init\n")
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
        meta_rows.append({
            "package": pkg,
            "module_name": module_name,
            "file_name": os.path.relpath(file_path, base_dir),
            "number_of_functions": function_est,
            "number_of_classes": 1,
            "total_lines": lines_count,
            "imports_count": imports_count,
            "complexity_estimate": random.randint(1,10)
        })
    mkdirp(os.path.dirname(metadata_path))
    with open(metadata_path, "w", newline='', encoding='utf-8') as mf:
        keys = ["package","module_name","file_name","number_of_functions","number_of_classes","total_lines","imports_count","complexity_estimate"]
        w = csv.DictWriter(mf, fieldnames=keys)
        w.writeheader()
        for r in meta_rows:
            w.writerow(r)

def make_zip(output_zip, base_dir):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(base_dir):
            for f in files:
                absf = os.path.join(root, f)
                arc = os.path.relpath(absf, base_dir)
                z.write(absf, arc)
    print(f"Created zip: {output_zip}")

def main(args):
    outdir = OUTPUT_DIR
    mkdirp(outdir)
    # Students / Courses / Enrollments
    students_file = os.path.join(outdir, "students.csv")
    courses_file = os.path.join(outdir, "courses.csv")
    enrollments_file = os.path.join(outdir, "enrollments.csv")
    print("Generating students...")
    generate_students(args.students, students_file)
    print("Generating courses...")
    generate_courses(args.courses, courses_file)
    print("Generating enrollments...")
    generate_enrollments(students_file, courses_file, args.enrollments, enrollments_file)
    # Video dataset
    video_courses_file = os.path.join(outdir, "video_courses.csv")
    videos_file = os.path.join(outdir, "videos.csv")
    transcripts_dir = os.path.join(outdir, "transcripts")
    print("Generating video courses...")
    generate_video_courses(args.video_courses, video_courses_file)
    print("Generating videos and transcripts...")
    generate_videos(args.videos, video_courses_file, videos_file, transcripts_dir)
    # Python modules
    py_base = os.path.join(outdir, "python_modules")
    py_meta = os.path.join(py_base, "modules_metadata.csv")
    print("Generating python modules...")
    generate_python_modules(args.py_modules, outdir, py_meta)
    # README
    readme_path = os.path.join(outdir, "README.txt")
    with open(readme_path, "w", encoding='utf-8') as r:
        r.write("Synthetic education datasets (Python) generated.\n")
        r.write(f"Students: {args.students}\nCourses: {args.courses}\nEnrollments: {args.enrollments}\n")
        r.write(f"Video courses: {args.video_courses}\nVideos: {args.videos}\nPython modules: {args.py_modules}\n")
    # Zip
    print("Creating ZIP...")
    make_zip(args.output, outdir)
    print("Done. You can upload the ZIP or extract the dataset directory to GitHub.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--students", type=int, default=1000, help="Number of students")
    ap.add_argument("--courses", type=int, default=100, help="Number of courses")
    ap.add_argument("--enrollments", type=int, default=5000, help="Number of enrollments")
    ap.add_argument("--video_courses", type=int, default=200, help="Number of video courses")
    ap.add_argument("--videos", type=int, default=1000, help="Number of videos")
    ap.add_argument("--py_modules", type=int, default=100, help="Number of python modules")
    ap.add_argument("--output", type=str, default="education-python-datasets.zip", help="Output ZIP filename")
    args = ap.parse_args()
    main(args)
