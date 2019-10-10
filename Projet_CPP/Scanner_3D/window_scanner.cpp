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

    m_filename->setMaxLength(10);
    m_filename->setMaximumWidth(150);

    m_button_Close->setMaximumWidth(150);
    //connect(m_button_Close, SIGNAL(clicked()), this, close());

    m_button_path->setMaximumWidth(150);
    connect(m_button_path, SIGNAL(clicked()), this, SLOT(recover_path()));

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

    m_button_rs->setMaximumWidth(150);
    connect(m_button_rs, SIGNAL(clicked()), this, SLOT(init_rs()));

    m_button_platform->setMaximumWidth(150);
    connect(m_button_platform, SIGNAL(clicked()), this, SLOT(init_platform()));

    m_button_start_scan->setMaximumWidth(150);
    connect(m_button_start_scan, SIGNAL(clicked()), this, SLOT(click_scan_platform()));

    m_button_stop_scan->setMaximumWidth(150);
    connect(m_button_stop_scan, SIGNAL(cliked()), this, SLOT(click_scan_stop()));

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

    m_button_rs2->setMaximumWidth(150);
    connect(m_button_rs2, SIGNAL(clicked()), this, SLOT(init_rs()));

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

    m_button_rs3->setMaximumWidth(150);
    connect(m_button_rs3, SIGNAL(clicked()), this, SLOT(init_rs()));

    m_button_start_scan2->setMaximumWidth(150);
    connect(m_button_start_scan2, SIGNAL(clicked()), this, SLOT(click_scan_mobile()));

    m_button_stop_scan2->setMaximumWidth(150);
    connect(m_button_stop_scan2, SIGNAL(cliked()), this, SLOT(click_scan_stop()));



    m_main_layout->addWidget(m_list_view);
    m_main_layout->addWidget(m_pcd);
    this->setLayout(m_main_layout);
}

Window_Scanner::~Window_Scanner()
{

}

void Window_Scanner::layout_mode_mobile()
{
    QVBoxLayout layout;
    QFormLayout layout_lim;

}

void Window_Scanner::layout_mode_platform()
{

}

void Window_Scanner::layout_mode_test()
{

}

void Window_Scanner::layout_logo_qt()
{

}

void Window_Scanner::layout_camera_view()
{

}

void Window_Scanner::layout_model_view()
{

}

void Window_Scanner::init_rs()
{

}

void Window_Scanner::recover_path()
{

}

void Window_Scanner::stream()
{

}

void Window_Scanner::click_scan_platform()
{

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
    i++;
}

void Window_Scanner::choose_resolution(int i)
{
    i++;
}

void Window_Scanner::choose_mode(int i)
{
    i++;
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
