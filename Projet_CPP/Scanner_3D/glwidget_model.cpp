#include "glwidget_model.h"

GLWidget_Model::GLWidget_Model()
{
    m_xRot = 0;
}

QSize GLWidget_Model::sizeHint()
{
    return QSize(1280, 1280);
}

void GLWidget_Model::paintGL(void){
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glPointSize(1);
    glRotated(180,1,0,0);
    glRotated(m_xRot/16,1,0,0);
    glRotated(m_yRot/16,0,1,0);

    /* A Finir */

    glEnableClientState(GL_VERTEX_ARRAY);
    glVertexPointer(3, GL_FLOAT,0, m_matrice);
    glDrawArrays(GL_POINTS, 0, 10);
    glDisableClientState(GL_VERTEX_ARRAY);

    glFlush();
}

void GLWidget_Model::setXRotation(double angle){
    m_xRot = angle;
    update();
}

void GLWidget_Model::setYRotation(double angle){
    m_yRot = angle;
    update();
}

void GLWidget_Model::mousePressEvent(QMouseEvent *event){

}

void GLWidget_Model::mouseMoveEvent(QMouseEventTransition *event){

}
