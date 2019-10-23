#include "window_scanner.h"

Window_Scanner::Window_Scanner(QWidget *parent)
    : QMainWindow(parent)
{
    m_list_view->insertItem(0, "LogoQT");
    m_list_view->insertItem(1, "vue Modèle");
    m_list_view->insertItem(2, "vue Caméra");
    m_list_view->setMaximumWidth(150);
    connect(m_list_view, SIGNAL(currentIndexChanged(int)), this,SLOT(choose_view(int)));

    m_list_mode->insertItem(0, "Platform");
    m_list_mode->insertItem(1, "Mobile");
    m_list_mode->insertItem(2, "Configurate Test");
    m_list_mode->setMaximumWidth(150);
    connect(m_list_mode, SIGNAL(currentIndexChanged(int)), this, SLOT(choose_mode(int)));

    m_list_resolution->insertItem(0, "720p");
    m_list_resolution->insertItem(1, "480p");
    m_list_resolution->insertItem(2, "360p");
    m_list_resolution->setMaximumWidth(150);
    connect(m_list_resolution, SIGNAL(currentIndexChanged(int)), this, SLOT(choose_resolution(int)));

    /*m_filename->setMaxLength(10);
    m_filename->setMaximumWidth(150);*/

    m_button_Close->setMaximumWidth(150);
    //connect(m_button_Close, SIGNAL(clicked()), this, close());

    m_button_path->setMaximumWidth(150);
    connect(m_button_path, SIGNAL(clicked()), this, SLOT(recover_path()));

    m_button_rs->setMaximumWidth(150);
    connect(m_button_rs, SIGNAL(clicked()), this, SLOT(init_rs()));

    m_stacked_gl->addWidget(m_logo_qt_widget);
    m_stacked_gl->addWidget(m_model_view_widget);
    m_stacked_gl->addWidget(m_camera_view_widget);

    //  Initialisation de la gestion des modes  //

    //  Mode Plateforme  //

    m_lim_y_high->setRange(0, 2);
    m_lim_y_high->setValue(0.5);
    m_lim_y_high->setDecimals(5);
    m_lim_y_high->setSingleStep(0.01);

    m_lim_y_low->setRange(0, 2);
    m_lim_y_low->setValue(0.5);
    m_lim_y_low->setDecimals(5);
    m_lim_y_low->setSingleStep(0.01);

    m_lim_z->setRange(0, 2);
    m_lim_z->setValue(0.5);
    m_lim_z->setDecimals(5);
    m_lim_z->setSingleStep(0.01);

    m_dist_center->setRange(0, 2);
    m_dist_center->setValue(0.35);
    m_dist_center->setDecimals(5);
    m_dist_center->setSingleStep(0.01);

    m_angle->setRange(0, 100);
    m_angle->setValue(3.6);
    m_angle->setDecimals(4);
    m_angle->setSingleStep(0.1);

    //connect progress bar

    m_button_save->setMaximumWidth(150);
    connect(m_button_save, SIGNAL(clicked()), this, SLOT(save_file()));

    m_button_platform->setMaximumWidth(150);
    connect(m_button_platform, SIGNAL(clicked()), this, SLOT(init_platform()));

    m_button_start_scan->setMaximumWidth(150);
    connect(m_button_start_scan, SIGNAL(clicked()), this, SLOT(click_scan_platform()));

    m_button_stop_scan->setMaximumWidth(150);
    //connect(m_button_stop_scan, SIGNAL(cliked()), this, SLOT(click_stop_scan()));

    //  Mode Test Plateforme  //

    m_lim_y_low_2->setRange(0, 2);
    m_lim_y_low_2->setValue(0.5);
    m_lim_y_low_2->setDecimals(5);
    m_lim_y_low_2->setSingleStep(0.01);

    m_lim_y_high_2->setRange(0, 2);
    m_lim_y_high_2->setValue(0.5);
    m_lim_y_high_2->setDecimals(5);
    m_lim_y_high_2->setSingleStep(0.01);

    m_lim_z2->setRange(0, 2);
    m_lim_z2->setValue(0.5);
    m_lim_z2->setDecimals(5);
    m_lim_z2->setSingleStep(0.01);

    m_dist_center2->setRange(0, 2);
    m_dist_center2->setValue(0.35);
    m_dist_center2->setDecimals(5);
    m_dist_center2->setSingleStep(0.01);

    m_angle2->setRange(0, 100);
    m_angle2->setValue(3.6);
    m_angle2->setDecimals(4);
    m_angle2->setSingleStep(0.1);

    m_button_test->setMaximumWidth(150);
    connect(m_button_test, SIGNAL(clicked()), this, SLOT(click_scan_test()));

    //  Mode Mobile  //

    m_lim_x3->setRange(0, 2);
    m_lim_x3->setValue(0.5);
    m_lim_x3->setDecimals(5);
    m_lim_x3->setSingleStep(0.01);

    m_lim_y3->setRange(0, 2);
    m_lim_y3->setValue(0.5);
    m_lim_y3->setDecimals(5);
    m_lim_y3->setSingleStep(0.01);

    m_lim_z3->setRange(0, 2);
    m_lim_z3->setValue(0.5);
    m_lim_z3->setDecimals(5);
    m_lim_z3->setSingleStep(0.01);

    m_button_save2->setMaximumWidth(150);
    connect(m_button_save2, SIGNAL(clicked()), this, SLOT(save_file()));

    m_button_start_scan2->setMaximumWidth(150);
    connect(m_button_start_scan2, SIGNAL(clicked()), this, SLOT(click_scan_mobile()));

    m_button_stop_scan2->setMaximumWidth(150);
    //connect(m_button_stop_scan2, SIGNAL(cliked()), this, SLOT(click_stop_scan()));

    layout_mode_platform();
    layout_mode_mobile();
    layout_mode_test();

    m_stacked_mode->addWidget(m_mode_platform_widget);
    m_stacked_mode->addWidget(m_mode_mobile_widget);
    m_stacked_mode->addWidget(m_mode_test_platform);

    QVBoxLayout *m_layout_box = new QVBoxLayout(this);

    QFormLayout *m_layout_choice = new QFormLayout(this);

    QHBoxLayout *m_layout_button = new QHBoxLayout(this);

    QVBoxLayout *m_layout_user = new QVBoxLayout(this);

    QVBoxLayout *m_main_layout = new QVBoxLayout(this);

    m_layout_box->addWidget(m_obj);
    m_layout_box->addWidget(m_pcd);
    m_layout_box->addWidget(m_stl);
    m_layout_box->addWidget(m_ply);
    m_layout_box->addWidget(m_vtk);

    m_layout_choice->addRow("Choice visu", m_list_view);
    m_layout_choice->addRow("Choice resolution", m_list_resolution);
    m_layout_choice->addRow("Choice 3D Format", m_layout_box);
    m_layout_choice->addRow("File Name", m_filename);
    m_layout_choice->addRow("Path Save", m_button_path);
    m_layout_choice->addRow("Connect Camera", m_button_rs);
    m_layout_choice->addRow("Mode Choice", m_list_mode);

    m_layout_button->addWidget(m_button_Close);

    m_layout_user->addLayout(m_layout_choice);
    m_layout_user->addWidget(m_stacked_mode);
    m_layout_user->addLayout(m_layout_button);

    m_main_layout->addWidget(m_stacked_gl);
    m_main_layout->addLayout(m_layout_user);

    QWidget *widget = new QWidget(this);
    widget->setWindowTitle("Scanner 3D");
    widget->setLayout(m_main_layout);

    setCentralWidget(widget);
    printf("ici");
}

Window_Scanner::~Window_Scanner()
{

}

void Window_Scanner::layout_mode_mobile()
{
    QVBoxLayout *layout = new QVBoxLayout();
    QFormLayout *layout_lim = new QFormLayout();
    layout_lim->addRow("Limite X", m_lim_x3);
    layout_lim->addRow("Limite Y", m_lim_y3);
    layout_lim->addRow("Limite Z", m_lim_z3);
    QHBoxLayout *layout_button = new QHBoxLayout();
    layout_button->addWidget(m_button_start_scan2);
    layout_button->addWidget(m_button_stop_scan2);
    layout_button->addWidget(m_button_save2);
    layout->addLayout(layout_lim);
    layout->addLayout(layout_button);
    m_mode_mobile_widget->setLayout(layout);

}

void Window_Scanner::layout_mode_platform()
{
    QVBoxLayout *layout = new QVBoxLayout();
    QFormLayout *layout_lim = new QFormLayout();
    QHBoxLayout *layout_button1 = new QHBoxLayout();
    QHBoxLayout *layout_button2 = new QHBoxLayout();
    layout_lim->addRow("Rotation Angle", m_angle);
    layout_lim->addRow("Limite Y High", m_lim_y_high);
    layout_lim->addRow("Limite Y Low", m_lim_y_low);
    layout_lim->addRow("Limite Z", m_lim_z);
    layout_lim->addRow("Center Distance", m_dist_center);
    layout_lim->addRow("Progress", m_progress);
    layout_button1->addWidget(m_button_platform);
    layout_button1->addWidget(m_button_start_scan);
    layout_button2->addWidget(m_button_save);
    layout_button2->addWidget(m_button_stop_scan);
    layout->addLayout(layout_lim);
    layout->addLayout(layout_button1);
    layout->addLayout(layout_button2);
    m_mode_platform_widget->setLayout(layout);
}

void Window_Scanner::layout_mode_test()
{
    QVBoxLayout *layout = new QVBoxLayout();
    QFormLayout *layout_lim = new QFormLayout();
    QHBoxLayout *layout_button1 = new QHBoxLayout();
    layout_lim->addRow("Rotation Angle", m_angle2);
    layout_lim->addRow("Limite Y High", m_lim_y_high_2);
    layout_lim->addRow("Limite Y Low", m_lim_y_low_2);
    layout_lim->addRow("Limite Z", m_lim_z2);
    layout_lim->addRow("Center Distance", m_dist_center2);
    layout_button1->addWidget(m_button_test);
    layout->addLayout(layout_lim);
    layout->addLayout(layout_button1);
    m_mode_test_platform->setLayout(layout);
}

void Window_Scanner::init_rs()
{
    m_rs->init_realsense();
}

void Window_Scanner::recover_path()
{

}

void Window_Scanner::stream()
{

}

void Window_Scanner::click_scan_platform()
{
    m_rs->recovery_platform_data_model();
}

void Window_Scanner::click_scan_mobile()
{

}

void Window_Scanner::click_scan_test()
{

}

void Window_Scanner::click_stop_scan()
{

}

void Window_Scanner::scan_platform()
{

}

void Window_Scanner::scan()
{

}

void Window_Scanner::closeEvent(QCloseEvent event)
{

}

void Window_Scanner::choose_view(int i)
{

}

void Window_Scanner::choose_resolution(int i)
{

}

void Window_Scanner::choose_mode(int i)
{
    m_stacked_mode->setCurrentIndex(i);
}

void Window_Scanner::save_file()
{

}

void Window_Scanner::init_platform()
{

}

void Window_Scanner::disable_to_scan()
{

}
