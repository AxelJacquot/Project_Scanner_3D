QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# The following define makes your compiler emit warnings if you use
# any Qt feature that has been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    glwidget_model.cpp \
    main.cpp \
    platform.cpp \
    realsense.cpp \
    window_scanner.cpp

HEADERS += \
    glwidget_model.h \
    include/librealsense2/h/rs_advanced_mode_command.h \
    include/librealsense2/h/rs_config.h \
    include/librealsense2/h/rs_context.h \
    include/librealsense2/h/rs_device.h \
    include/librealsense2/h/rs_frame.h \
    include/librealsense2/h/rs_internal.h \
    include/librealsense2/h/rs_option.h \
    include/librealsense2/h/rs_pipeline.h \
    include/librealsense2/h/rs_processing.h \
    include/librealsense2/h/rs_record_playback.h \
    include/librealsense2/h/rs_sensor.h \
    include/librealsense2/h/rs_types.h \
    include/librealsense2/hpp/rs_context.hpp \
    include/librealsense2/hpp/rs_device.hpp \
    include/librealsense2/hpp/rs_export.hpp \
    include/librealsense2/hpp/rs_frame.hpp \
    include/librealsense2/hpp/rs_internal.hpp \
    include/librealsense2/hpp/rs_options.hpp \
    include/librealsense2/hpp/rs_pipeline.hpp \
    include/librealsense2/hpp/rs_processing.hpp \
    include/librealsense2/hpp/rs_record_playback.hpp \
    include/librealsense2/hpp/rs_sensor.hpp \
    include/librealsense2/hpp/rs_types.hpp \
    include/librealsense2/rs.h \
    include/librealsense2/rs.hpp \
    include/librealsense2/rs_advanced_mode.h \
    include/librealsense2/rs_advanced_mode.hpp \
    include/librealsense2/rsutil.h \
    platform.h \
    realsense.h \
    window_scanner.h

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

INCLUDEPATH += ./include/librealsense2 \
               ./include/librealsense2/hpp \
               ./include/librealsense2/h \

LIBS += /usr/local/lib/librealsense2.so #pc
