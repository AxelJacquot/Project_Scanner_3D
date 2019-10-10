#include "window_scanner.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Window_Scanner w;
    w.show();
    return a.exec();
}
