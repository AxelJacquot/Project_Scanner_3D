#ifndef GLWIDGET_MODEL_H
#define GLWIDGET_MODEL_H

#include <QOpenGLWidget>
#include <QSize>
#include <QMouseEvent>
#include <QMouseEventTransition>
#include <GL/gl.h>

class GLWidget_Model : public QOpenGLWidget
{
public:
    GLWidget_Model();
    QSize sizeHint(void);
    void paintGL(void);
    void setXRotation(double angle);
    void setYRotation(double angle);
    void mousePressEvent(QMouseEvent *event);
    void mouseMoveEvent(QMouseEventTransition *event);


public slots:
    void set_data(double *matrice);

private:
    double m_xRot = 0;
    double m_yRot = 0;
    double m_zRot = 0;
    QPoint m_lastPos;
    double *m_matrice;


    
};

#endif // GLWIDGET_MODEL_H
