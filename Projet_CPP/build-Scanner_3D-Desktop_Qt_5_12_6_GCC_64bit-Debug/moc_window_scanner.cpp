/****************************************************************************
** Meta object code from reading C++ file 'window_scanner.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.12.6)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../Scanner_3D/window_scanner.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'window_scanner.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.12.6. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_Window_Scanner_t {
    QByteArrayData data[19];
    char stringdata0[228];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_Window_Scanner_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_Window_Scanner_t qt_meta_stringdata_Window_Scanner = {
    {
QT_MOC_LITERAL(0, 0, 14), // "Window_Scanner"
QT_MOC_LITERAL(1, 15, 7), // "init_rs"
QT_MOC_LITERAL(2, 23, 0), // ""
QT_MOC_LITERAL(3, 24, 12), // "recover_path"
QT_MOC_LITERAL(4, 37, 19), // "click_scan_platform"
QT_MOC_LITERAL(5, 57, 17), // "click_scan_mobile"
QT_MOC_LITERAL(6, 75, 15), // "click_scan_test"
QT_MOC_LITERAL(7, 91, 15), // "click_stop_scan"
QT_MOC_LITERAL(8, 107, 13), // "scan_platform"
QT_MOC_LITERAL(9, 121, 4), // "scan"
QT_MOC_LITERAL(10, 126, 10), // "closeEvent"
QT_MOC_LITERAL(11, 137, 12), // "QCloseEvent*"
QT_MOC_LITERAL(12, 150, 5), // "event"
QT_MOC_LITERAL(13, 156, 17), // "choose_resolution"
QT_MOC_LITERAL(14, 174, 1), // "i"
QT_MOC_LITERAL(15, 176, 11), // "choose_mode"
QT_MOC_LITERAL(16, 188, 9), // "save_file"
QT_MOC_LITERAL(17, 198, 13), // "init_platform"
QT_MOC_LITERAL(18, 212, 15) // "disable_to_scan"

    },
    "Window_Scanner\0init_rs\0\0recover_path\0"
    "click_scan_platform\0click_scan_mobile\0"
    "click_scan_test\0click_stop_scan\0"
    "scan_platform\0scan\0closeEvent\0"
    "QCloseEvent*\0event\0choose_resolution\0"
    "i\0choose_mode\0save_file\0init_platform\0"
    "disable_to_scan"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_Window_Scanner[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      14,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   84,    2, 0x0a /* Public */,
       3,    0,   85,    2, 0x0a /* Public */,
       4,    0,   86,    2, 0x0a /* Public */,
       5,    0,   87,    2, 0x0a /* Public */,
       6,    0,   88,    2, 0x0a /* Public */,
       7,    0,   89,    2, 0x0a /* Public */,
       8,    0,   90,    2, 0x0a /* Public */,
       9,    0,   91,    2, 0x0a /* Public */,
      10,    1,   92,    2, 0x0a /* Public */,
      13,    1,   95,    2, 0x0a /* Public */,
      15,    1,   98,    2, 0x0a /* Public */,
      16,    0,  101,    2, 0x0a /* Public */,
      17,    0,  102,    2, 0x0a /* Public */,
      18,    0,  103,    2, 0x0a /* Public */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 11,   12,
    QMetaType::Void, QMetaType::Int,   14,
    QMetaType::Void, QMetaType::Int,   14,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void Window_Scanner::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<Window_Scanner *>(_o);
        Q_UNUSED(_t)
        switch (_id) {
        case 0: _t->init_rs(); break;
        case 1: _t->recover_path(); break;
        case 2: _t->click_scan_platform(); break;
        case 3: _t->click_scan_mobile(); break;
        case 4: _t->click_scan_test(); break;
        case 5: _t->click_stop_scan(); break;
        case 6: _t->scan_platform(); break;
        case 7: _t->scan(); break;
        case 8: _t->closeEvent((*reinterpret_cast< QCloseEvent*(*)>(_a[1]))); break;
        case 9: _t->choose_resolution((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 10: _t->choose_mode((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 11: _t->save_file(); break;
        case 12: _t->init_platform(); break;
        case 13: _t->disable_to_scan(); break;
        default: ;
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject Window_Scanner::staticMetaObject = { {
    &QMainWindow::staticMetaObject,
    qt_meta_stringdata_Window_Scanner.data,
    qt_meta_data_Window_Scanner,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *Window_Scanner::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *Window_Scanner::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_Window_Scanner.stringdata0))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int Window_Scanner::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 14)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 14;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 14)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 14;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE