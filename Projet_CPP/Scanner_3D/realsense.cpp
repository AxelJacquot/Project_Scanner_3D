#include "realsense.h"
#include <iostream>

using namespace std;


RealSense::RealSense()
{

}

void RealSense::init_realsense()
{
    rs_config.enable_stream(RS2_STREAM_DEPTH, m_width, m_height, RS2_FORMAT_Z16, 30);
    rs_config.enable_stream(RS2_STREAM_COLOR, m_width, m_height, RS2_FORMAT_RGB8, 30);
    rs_pipe.start(rs_config);
    connect = true;
    //filter();
}

void RealSense::profile_stop()
{
    rs_pipe.stop();
    rs_config.disable_all_streams();
}

void RealSense::set_resolution(unsigned short width, unsigned short height)
{
    m_width = width;
    m_height = height;
}

void RealSense::filter()
{
    rs2::decimation_filter decimate;
    decimate.set_option(RS2_OPTION_FILTER_MAGNITUDE,0.0);

    //Add filter
}

void RealSense::set_mode_platfrom()
{

}

void RealSense::recovery_platform_data_model()
{
    rs2::points points;
    rs2::frameset frame;
    frame = rs_pipe.wait_for_frames();
    rs2::depth_frame depth_frame = frame.get_depth_frame();
    points = rs2::pointcloud().calculate(depth_frame);
    const rs2::vertex* data = points.get_vertices();
    unsigned long size = points.size();
    for(unsigned long i=0; i<size; i++){
        cout << data->x << endl;
        data++;
    }
    cout << size << endl;

}

void RealSense::recovery_mobile_data_model()
{

}

bool RealSense::getConnect() const
{
    return connect;
}

