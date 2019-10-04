#ifndef SCANNER_WINDOW_H
#define SCANNER_WINDOW_H

#include <QMainWindow>

class Scanner_window : public QMainWindow
{
    Q_OBJECT

public:
    Scanner_window(QWidget *parent = nullptr);
    ~Scanner_window();
};
#endif // SCANNER_WINDOW_H
