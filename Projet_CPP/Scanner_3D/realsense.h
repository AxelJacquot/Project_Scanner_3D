#ifndef REALSENSE_H
#define REALSENSE_H

//#include <librealsense2/rs.h>
#include <rs.hpp>
#include <QWidget>

class RealSense
{
public:
    RealSense();

    void init_realsense(void);
    void profile_stop(void);
    void set_resolution(unsigned short width, unsigned short height);
    void filter(void);
    void recovery_platform_data_model(void);
    void recovery_mobile_data_model(void);
    void set_mode_platfrom(void);
    void set_mode_mobile(void);
    void set_mode_test(void);

private:
   bool platform = true;
   bool mobile = false;

   unsigned short m_width = 1280;
   unsigned short m_height = 720;

   rs2::config rs_config;
   rs2::pipeline rs_pipe;

};

#endif // REALSENSE_H
