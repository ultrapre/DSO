#include "mainwindow.h"
#include "ui_mainwindow.h"
//#include <algorithm>
#include <QDebug>
#include <QFile>
//#include <QSettings>
#include <QString>
//#include <QStringList>
//#include <QRegExp>
//#include <QDir>

#include <QtCore/qmath.h>
//#include<QDebug>
//#include<QStringList>
//#include<QString>
//#include <QFile>
//#include <QMessageBox>
QString csvfile = "ngcic.csv";

//#include "vecmath.h"

//typedef Vector3<double>	Vec3d;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void readNGC(QDataStream& in)
{
    bool isIc;
    int nb;
    float ra, dec;
    unsigned int type;

    float mag;                      // Apparent magnitude
    float angularSize;              // Angular size in degree


    in >> isIc >> nb >> ra >> dec >> mag >> angularSize >> type;
    qDebug()<< isIc << nb << ra << dec << mag << angularSize << type;


}

bool loadNGC(const QString& catNGC)
{
    QFile in(catNGC);
    if (!in.open(QIODevice::ReadOnly))
        return false;
    QDataStream ins(&in);
    ins.setVersion(QDataStream::Qt_4_5);

    int totalRecords=0;
    while (!ins.atEnd())
    {
        // Create a new Nebula record
        //NebulaP e = NebulaP(new Nebula);
        //e->readNGC(ins);
        readNGC(ins);

        //nebArray.append(e);
        //nebGrid.insert(qSharedPointerCast<StelRegionObject>(e));
        //if (e->NGC_nb!=0)
        //    ngcIndex.insert(e->NGC_nb, e);
        ++totalRecords;
    }
    in.close();
    //qDebug() << "Loaded" << totalRecords << "NGC records";
    return true;
}

bool dumpNGC(const QString& catNGC)
{

    bool isIc;
    int nb;
    float ra, dec;
    unsigned int type;
    float mag;                      // Apparent magnitude
    float angularSize;              // Angular size in degree


    int totalRecords=0;

    const QString FILE_PATH(csvfile);
    QFile csvFile(FILE_PATH);
    QStringList CSVList;
    CSVList.clear();

    if (csvFile.open(QIODevice::ReadWrite))
    {
        QTextStream stream(&csvFile);

        while (!stream.atEnd())
        {
            CSVList.push_back(stream.readLine());
        }

        csvFile.close();
    }

    /**/
    QFile in(catNGC);
    if (!in.open(QIODevice::WriteOnly))
        return false;
    QDataStream ins(&in);
    ins.setVersion(QDataStream::Qt_4_5);
    /**/

    Q_FOREACH(QString str, CSVList)
    {
        isIc = str.split(",")[0] == "NGC" ? false : true;
        nb = str.split(",")[1].toInt();
        ra = str.split(",")[2].toFloat();
        dec = str.split(",")[3].toFloat();
        mag = str.split(",")[4].toFloat();
        angularSize = str.split(",")[5].toFloat();
        type = str.split(",")[6].toInt();

        ins << isIc << nb << ra << dec << mag << angularSize << type;

       // qDebug()<< isIc << nb << ra << dec << mag << angularSize << type;
        ++totalRecords;
    }


    in.close();
    //qDebug() << "Dumped" << totalRecords << "NGC records";
    return true;
}

void MainWindow::on_pushButton_clicked()
{
    loadNGC("ngc2000.dat");
}

void MainWindow::on_pushButton_2_clicked()
{
    dumpNGC("ngc2000new.dat");
}
