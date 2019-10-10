#ifndef WINDOW_SCANNER_H
#define WINDOW_SCANNER_H

#include <QMainWindow>
#include <QHBoxLayout>
#include <QSlider>
#include <QPushButton>
#include <QCheckBox>
#include <QLabel>
#include <QComboBox>
#include <QVBoxLayout>
#include <QMessageBox>
#include <QSpinBox>
#include <QLineEdit>
#include <QStackedWidget>
#include <QFormLayout>
#include <QDesktopWidget>
#include <QFileDialog>
#include <QDoubleSpinBox>
#include <QProgressBar>
#include <QTimer>
#include <QCloseEvent>
#include <QProgressBar>
#include <QLayout>
#include <Qt>

#include <glwidget.h>
#include <glwidget_camera.h>
#include <glwidget_model.h>
#include <platform.h>
#include <realsense.h>

class Window_Scanner : public QMainWindow
{
    Q_OBJECT

public:
    Window_Scanner(QWidget *parent = nullptr);
    ~Window_Scanner(void);

    void layout_mode_mobile(void);
    void layout_mode_platform(void);
    void layout_mode_test(void);

    void layout_logo_qt(void);
    void layout_camera_view(void);
    void layout_model_view(void);



public slots:
    void init_rs(void);

    void recover_path(void);
    void stream(void);

    void click_scan_platform(void);
    void click_scan_mobile(void);
    void click_scan_test(void);
    void click_stop_scan(void);

    void scan_platform(void);
    void scan(void);

    void closeEvent(QCloseEvent event);

    void choose_view(int i);

    void choose_resolution(int i);

    void choose_mode(int i);

    void save_file(void);

    void init_platform(void);

    void disable_to_scan(void);

private:
    bool connect_rs = false;
    QString m_out = "";
    QString m_port = "";

    RealSense m_rs;

    QTimer m_timer;

    QComboBox *m_list_view = new QComboBox(this);
    QComboBox *m_list_resolution = new QComboBox(this);
    QComboBox *m_list_mode = new QComboBox(this);

    GLWidget *m_glwidget = new GLWidget();
    GLWidget_Camera *m_glwidget_Camera = new GLWidget_Camera();
    GLWidget_Model *m_glwidget_Model = new GLWidget_Model();
    QWidget *m_camera_view_widget = new QWidget(this);
    QWidget *m_model_view_widget = new QWidget(this);
    QWidget *m_logo_qt_widget = new QWidget(this);
    QStackedWidget *m_stacked_gl = new QStackedWidget(this);

    QCheckBox *m_pcd = new QCheckBox("PCD", this);
    QCheckBox *m_obj = new QCheckBox("OBJ", this);
    QCheckBox *m_stl = new QCheckBox("STL", this);
    QCheckBox *m_ply = new QCheckBox("STL", this);
    QCheckBox *m_vtk = new QCheckBox("VTK", this);

    QLineEdit *m_filename;
    QPushButton *m_button_Close = new QPushButton("Close", this);
    QPushButton *m_button_path = new QPushButton("Chemin", this);

    QDoubleSpinBox *m_angle = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_dist_center = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_lim_y_high = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_lim_y_low = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_lim_z = new QDoubleSpinBox(this);
    QProgressBar *m_progress = new QProgressBar(this);
    QPushButton *m_button_save = new QPushButton("Save", this);
    QPushButton *m_button_rs = new QPushButton("Connect Camera", this);
    QPushButton *m_button_start_scan = new QPushButton("Start Scan", this);
    QPushButton *m_button_stop_scan = new QPushButton("Stop Scan", this);
    QPushButton *m_button_platform = new QPushButton("Connect Platform", this);

    QDoubleSpinBox *m_angle2 = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_dist_center2 = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_lim_y_high_2 = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_lim_y_low_2 = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_lim_z2 = new QDoubleSpinBox(this);
    QPushButton *m_button_rs2 = new QPushButton("Connect Camera", this);
    QPushButton *m_button_test = new QPushButton("Start_test", this);

    QDoubleSpinBox *m_lim_x3 = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_lim_y3 = new QDoubleSpinBox(this);
    QDoubleSpinBox *m_lim_z3 = new QDoubleSpinBox(this);
    QPushButton *m_button_save2 = new QPushButton("Save", this);
    QPushButton *m_button_rs3 = new QPushButton("Connect Camera", this);
    QPushButton *m_button_start_scan2 = new QPushButton("Start Scan", this);
    QPushButton *m_button_stop_scan2 = new QPushButton("Stop Scan", this);

    QWidget *m_mode_platform_widget = new QWidget();
    QWidget *m_mode_mobile_widget = new QWidget();
    QWidget *m_mode_test_platform = new QWidget();
    QStackedWidget *m_stacked_mode = new QStackedWidget(this);



};

#endif // WINDOW_SCANNER_H
