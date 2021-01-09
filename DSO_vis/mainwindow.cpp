#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QtCore/qmath.h>
#include<QDebug>
#include<QStringList>
#include<QString>
#include <QFile>

QString csvfile = "Messier.csv";

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->AOD1->setText("0");

//    ui->mag1->setText("9.7");
//    ui->longax1->setText("7.4");
//    ui->shortax1->setText("5.1");
    ui->diame1->setText("80");
    ui->focal1->setText("400");
    ui->eyefo1->setText("20");
    ui->skybr1->setText("20.5");

}

MainWindow::~MainWindow()
{
    delete ui;
}

double visCalculate(double mag1, double longax1, double shortax1, double diamet1, double focal1, double eyefo1, double skysur1,double AOD){
    double objsrfb = mag1 + 2.5*qLn(2827*longax1*shortax1)/qLn(10);

    if(AOD > 0 && AOD < 1){
        objsrfb = objsrfb - 2.5*qLn(1-AOD)/qLn(10);
    }

    double magnif = focal1/eyefo1;

    double appsize = sqrt(longax1*shortax1)*magnif;

    double exitpur = diamet1/magnif;

    double dimmi = 5*qLn(7/exitpur)/qLn(10);

    double objrslbr = objsrfb + dimmi;

    double skyrslbr = skysur1 + dimmi;

    double b0 = sqrt(7.5*qLn(appsize/15)/qLn(10)+0.45)+19.3;

    double sss = 0.42+0.155*qLn(appsize/15)/qLn(10);

    double E1 = 0.35;

    double threshold = sss*(skyrslbr-19)+b0-E1*(pow((skyrslbr/24),5));

    double contrast = threshold - objrslbr;

    return contrast;
}

void MainWindow::on_pushButton_clicked()
{
    if(ui->radioButton->isChecked()){
        double mag1 = ui->mag1->text().trimmed().toDouble();
        double longax1 = ui->longax1->text().trimmed().toDouble();
        double shortax1 = ui->shortax1->text().trimmed().toDouble();
        double diamet1 = ui->diame1->text().trimmed().toDouble();
        double focal1 = ui->focal1->text().trimmed().toDouble();
        double eyefo1 = ui->eyefo1->text().trimmed().toDouble();
        double skysur1 = ui->skybr1->text().trimmed().toDouble();

        double AOD = ui->AOD1->text().trimmed().toDouble();



        double contrast = visCalculate(mag1,longax1,shortax1,diamet1,focal1,eyefo1,skysur1,AOD);

//        qDebug()<<mag1<<longax1<<shortax1<<diamet1<<focal1<<eyefo1<<skysur1;

        qDebug()<<contrast;

        ui->contr->setText(QString::number(contrast));




        //double tmp = pow((skyrslbr/24),5);




    }
    else{

    }
}



void MainWindow::on_pushButton_2_clicked()
{
    if(ui->checkBoxclear->isChecked()){
        ui->textBrowser->clear();
    }
//    ui->textBrowser->append("good\n");
    if(ui->radioButton_3->isChecked()){
        csvfile = "Messier.csv";
    }
    else if (ui->radioButton_4->isChecked()) {
        csvfile = "Herschel400.csv";
    }
    else if (ui->radioButton_5->isChecked()) {
        csvfile = "NGC.csv";
    }
    else if (ui->radioButton_6->isChecked()) {
        csvfile = ui->mycsvfile->text();
    }

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
    ui->textBrowser->append( "Object\tContrast");
    Q_FOREACH(QString str, CSVList)
    {
        QString obj = str.split(",")[0];
        QString bright = str.split(",")[1];
        QString length = str.split(",")[2];
        QString width = str.split(",")[3];

        double mag1 = bright.toDouble();
        double longax1 = length.toDouble();
        double shortax1 = width.toDouble();

        double diamet1 = ui->diame1->text().trimmed().toDouble();
        double focal1 = ui->focal1->text().trimmed().toDouble();
        double eyefo1 = ui->eyefo1->text().trimmed().toDouble();
        double skysur1 = ui->skybr1->text().trimmed().toDouble();
        double AOD = ui->AOD1->text().trimmed().toDouble();
        double contrast = visCalculate(mag1,longax1,shortax1,diamet1,focal1,eyefo1,skysur1,AOD);
        if (contrast > 0){
//            qDebug() << obj<<" "<<bright<<" "<<length<<" "<<width<<"\n";
            ui->textBrowser->append( obj+"\t"+QString::number(contrast));
        }

    }
}

void MainWindow::on_radioButton_6_clicked()
{
    if(ui->radioButton_6->isChecked()){
        ui->mycsvfile->setVisible(true);
    }
    else {
        ui->mycsvfile->setVisible(false);
    }
}

void MainWindow::on_pushButton_3_clicked()
{
    ui->textBrowser->clear();
}

void MainWindow::on_comboBox_currentIndexChanged(const QString &arg1)
{
    if(ui->comboBox->currentText()=="20×80双筒"){
        ui->diame1->setText("80");
        ui->focal1->setText("400");
        ui->eyefo1->setText("20");
    }
    else if(ui->comboBox->currentText()=="星达150750"){
        ui->diame1->setText("150");
        ui->focal1->setText("750");
        ui->eyefo1->setText("20");

    }
    else if(ui->comboBox->currentText()=="DOB16"){
        ui->diame1->setText("400");
        ui->focal1->setText("1600");
        ui->eyefo1->setText("20");
    }
}
