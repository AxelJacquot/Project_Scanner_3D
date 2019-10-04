#include "scanner_window.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Scanner_window w;
    w.show();
    return a.exec();
}
