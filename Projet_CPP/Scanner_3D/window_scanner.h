#ifndef WINDOW_SCANNER_H
#define WINDOW_SCANNER_H

#include <QMainWindow>
#include<QHBoxLayout>
#include<QSlider>
#include<QPushButton>
#include<QCheckBox>
#include<QLabel>
#include<QComboBox>
#include<QVBoxLayout>
#include<QMessageBox>
#include<QSpinBox>
#include<QLineEdit>
#include<QStackedWidget>
#include<QFormLayout>
#include<QDesktopWidget>
#include<QFileDialog>
#include<QDoubleSpinBox>
#include<QProgressBar>
#include<QTimer>
#include<QCloseEvent>
#include<glwidget.h>
#include<glwidget_camera.h>
#include<glwidget_model.h>
#include<platform.h>

class Window_Scanner : public QMainWindow
{
    Q_OBJECT

public:
    Window_Scanner(QWidget *parent = nullptr);
    ~Window_Scanner();

    void layout_mode_mobile(void);
    void layout_mode_platform(void);
    void layout_mode_test(void);

    void layout_logo_qt(void);
    void layout_camera_view(void);
    void layout_model_view(void);

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

    void choose_view(char i);

    void choose_resolution(char i);

    void choose_mode(char i);

    void save_file(void);

    void init_platform(void);

    void disable_to_scan(void);

private:
    bool connect_rs;
    QString m_out = "";
    QString m_port = "";



    QTimer m_timer();

    QComboBox m_list_view();
    QComboBox m_list_resolution();
    QComboBox m_list_mode();

    GLWidget m_glwidget();
    GLWidget_Camera m_glwidget_();
    GLWidget_Model m_glwidget_model();
    QWidget m_camera_view_widget();
    QWidget m_model_view_widget();
    QWidget m_logo_qt_widget();
    QStackedWidget m_stacked_gl();

    QCheckBox m_pcd();
    QCheckBox m_obj();
    QCheckBox m_stl();
    QCheckBox m_ply();
    QCheckBox m_vtk();

    QLineEdit m_filename();
    QPushButton m_button_path();

    QDoubleSpinBox m_angle();
    QDoubleSpinBox m_dist_center();
    QDoubleSpinBox m_lim_y_high();
    QDoubleSpinBox m_lim_y_low();
    QDoubleSpinBox m_lim_z();
    QPushButton m_button_save();
    QPushButton m_button_rs();
    QPushButton m_button_start_scan();
    QPushButton m_button_stop_scan();
    QPushButton m_button_platform();

    QDoubleSpinBox m_angle2();
    QDoubleSpinBox m_dist_center2();
    QDoubleSpinBox m_lim_y_high_2();
    QDoubleSpinBox m_lim_y_low_2();
    QDoubleSpinBox m_lim_z2();
    QPushButton m_button_rs2();

    QDoubleSpinBox m_lim_x3();
    QDoubleSpinBox m_lim_y3();
    QDoubleSpinBox m_lim_z3();
    QPushButton m_button_save2();
    QPushButton m_button_rs3();
    QPushButton m_button_start_scan2();
    QPushButton m_button_stop_scan2();

    QWidget m_mode_platform_widget();
    QWidget m_mode_mobile_widget();
    QWidget m_mode_test_platform();
    QStackedWidget m_stacked_mode();

    QVBoxLayout m_layout_box();

    QFormLayout m_layout_choice();

    QHBoxLayout m_layout_button();

    QVBoxLayout m_layout_final();


};

#endif // WINDOW_SCANNER_H
