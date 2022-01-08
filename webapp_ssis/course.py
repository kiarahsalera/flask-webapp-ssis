from flask import Blueprint, render_template, redirect, url_for, request
import webapp_ssis.functions as db


course = Blueprint('course', __name__)


@course.route("/course", methods=['GET', 'POST'])
def displayCoursePage():
    course = db.Course.display_course()
    student = db.Student.display_students()
    college = db.College.display_college()
    return render_template('course.html', 
                                data = [course,student,college],
                                datacount = f'{len(course)} Course')

@course.route('/course/search', methods=['GET', 'POST'])
def search() -> str:
    if request.method == 'POST':

        user_input = request.form.get('user-input')
        field = request.form.get('field')
        print(user_input,field)

        if field == 'select':
            result = db.Course().search(keyword=user_input)
        elif field == 'code':
            result = db.Course().search(keyword=user_input, field='code')
        elif field == 'code_name':
            result = db.Course().search(keyword=user_input, field='code_name')
        elif field == 'college_name':
            result = db.Course().search(keyword=user_input, field='college_name')
        else:
            result = []

        if len(result) != 0:
            return render_template('course.html', 
                                    data=[result],
                                    datacount = f'Search Result: {len(result)}'
                                   )
    else:
        return redirect(url_for('course.displayCoursePage'))



@course.route("/course/add_course", methods=['GET', 'POST'])
def addCourse():
    if request.method == "POST":
        code = request.form['code'].upper()
        code_name = request.form['code_name'].capitalize()
        college_name = request.form['college_name'].upper()

     

        course = db.Course(code, code_name, college_name)
        course.add_course()
        return redirect(url_for('course.displayCoursePage'))

@course.route('/course/delete/<string:code>')
def delete(code: str) -> str:
    db.Course().delete(code)
    
    return redirect(url_for("course.displayCoursePage"))

@course.route("/course/edit_course", methods=['GET', 'POST'])
def editCourse():
    if request.method == "POST":
        old_course_number = request.form['old_course_number']
        code = request.form['code'].upper()
        code_name = request.form['code_name'].capitalize()
        college_name = request.form['college_name'].upper()
        


        db.Course.edit_course(code, code_name, college_name, old_course_number)
        return redirect(url_for('course.displayCoursePage'))

