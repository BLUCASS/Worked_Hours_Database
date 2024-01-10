from model import engine, Job, MyJob
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class Daytime:
    
    def __day(self) -> str:
        from datetime import datetime, timedelta
        while True:
            try:
                date_user = input(str('Type the day (DD/MM/YYYY): '))
                date = datetime.strptime(date_user, '%d/%m/%Y').date()
            except:
                print('\033[31mPLEASE, INSERT THE DATE CORRECTLY (DD/MM/YYYY)\033[m')
                continue
            else:
                days = {}
                for i in range(7):
                    next_date = date + timedelta(days=i)
                    days[next_date.strftime('%A')] = next_date
                return days

    def __salary(self) -> float:
        while True:
            try:
                salary = float(input('Type your salary: '))
            except:
                print('\033[31mINVALID VALUE\033[m')
            else:
                return salary

    def __sunday_salary(self) -> float:        
        while True:
            try:
                salary = float(input('Type your salary on Sunday: '))
            except:
                print('\033[31mINVALID VALUE\033[m')
            else:
                return salary

    def __hours_converter(self, seconds):
        horas = seconds // 3600
        min = (seconds % 3600) // 60
        seg = seconds % 60
        return str(horas) + ':' + str(min) + ':' + str(seg)

    def __choose_person(self) -> int:
        try:
            person = int(input('[1] Person1\n[2] Person2\nChoose the person: '))
        except:
            print('\033[31mINVALID OPTION\033[m')
        else:
            return person

    def hours (self) -> str:
        from datetime import datetime
        whole_week = self.__day()
        week = []
        total_hours = total_week = total_money = hours_week = 0
        regular_salary = self.__salary()
        sunday_salary = self.__sunday_salary()
        person = self.__choose_person()
        for day, date in whole_week.items():
            while True:
                try:
                    clockin = input(str(f'Clockin on {day} [Hour:Min]: '))
                    clockin_format = datetime.strptime(clockin, '%H:%M')
                except:
                    print('\033[31mINVALID FORMAT\033[m')
                    continue
                else:
                    break
            while True:
                try:    
                    clockout = input(str(f'Clockout on {day} [Hour:Min]: '))
                    clockout_format = datetime.strptime(clockout, '%H:%M')
                except:
                    print('\033[31mINVALID FORMAT\033[m')
                    continue
                else:
                    break
            sum_tot_day = clockout_format - clockin_format
            total_hours = int(sum_tot_day.total_seconds())
            hours_week += total_hours
            hours = self.__hours_converter(total_hours)
            if day == 'Sunday':
                salary = sunday_salary
                total_day = (sum_tot_day.total_seconds()/3600) * sunday_salary
            else:
                salary = regular_salary
                total_day = (sum_tot_day.total_seconds()/3600) * salary
            total_money += total_day
            total_week = self.__hours_converter(hours_week)
            if person == 1:
                db = Job(date=date,
                            day=day,
                            hours=hours,
                            tot_hours=total_week,
                            salary=salary,
                            tot_day=total_day,
                            tot_week=total_money)
            elif person == 2:
                db = MyJob(date=date,
                            day=day,
                            hours=hours,
                            tot_hours=total_week,
                            salary=salary,
                            tot_day=total_day,
                            tot_week=total_money)
            week.append(db)
        for db in week:
            self.__add_db(db)

    def __add_db(self, arg: Job) -> None:
        try:
            session.add(arg)
        except:
            session.rollback()
            return f'\033[31mERROR. DATA NOT ADDED TO THE DATABASE.\033[m'
        else:
            session.commit()
            return f'\033[32mSUCCESSFULLY ADDED TO THE DATABASE\033[m'
        finally:
            session.close()

    def read_db(self):
        from time import sleep
        person = self.__choose_person()
        if person == 1:
            data = session.query(Job).all()
        elif person == 2:
            data = session.query(MyJob).all()
        print(f'\033[1;42m {"DATE":<13}{"DAY":<12}{"HOURS":<7}{"TOTAL HOURS":<14}{"SALARY":<9}{"SALARY DAY":<12}{"TOTAL WEEK":<11}\033[m')
        for line in data:
            print(f' {line.date:<13}{line.day:<12}{line.hours:<9}{line.tot_hours:<12}€ {line.salary:<7.1f}€ {line.tot_day:<10.2f}€ {line.tot_week:<7.2f}')
        sleep(3)
        session.close()

    def read_week(self) -> None:
        from datetime import timedelta
        from time import sleep
        date_user = self.__get_date()
        week = [date_user, date_user + timedelta(days=1), date_user + timedelta(days=2), date_user + timedelta(days=3),
                date_user + timedelta(days=4), date_user + timedelta(days=5), date_user + timedelta(days=6)]
        person = self.__choose_person()
        try:
            if person == 1:
                data = session.query(Job).filter(or_(Job.date == week[0], Job.date ==  week[1], Job.date == week[2], Job.date == week[3],
                                            Job.date == week[4], Job.date == week[5], Job.date == week[6]))
            elif person == 2:
                data = session.query(MyJob).filter(or_(MyJob.date == week[0], MyJob.date == week[1], MyJob.date == week[2],
                MyJob.date == week[3], MyJob.date == week[4], MyJob.date == week[5], MyJob.date == week[6]))
        except Exception as erro:
            print(erro)
            print('\033[31mINVALID DATA\033[m')
        else:
            print (f'\033[1;42m {"DATE":<13}{"DAY":<12}{"HOURS":<7}{"TOTAL HOURS":<14}{"SALARY":<9}{"SALARY DAY":<12}{"TOTAL WEEK":<11}\033[m')
            for line in data:
                print(f' {line.date:<13}{line.day:<12}{line.hours:<9}{line.tot_hours:<12}€ {line.salary:<7.1f}€ {line.tot_day:<10.2f}€ {line.tot_week:<7.2f}')
            sleep(3)
            session.close()
        
    def deleting_values(self) -> None:
        date_user = self.__get_date()
        person = self.__choose_person()
        if person == 1:
            data = session.query(Job).filter(Job.date == date_user).first()
        elif person == 2:
            data = session.query(MyJob).filter(MyJob.date == date_user).first()
        try:
            session.delete(data)
        except:
            print('\033[31mDATA NOT FOUND.\033[m')
            session.rollback()
        else:
            print('\033[32mSUCCESSFULLY DELETED\033[m')
            session.commit()
        finally:
            session.close()

    def __get_date(self) -> str:
        from datetime import datetime, date
        while True:
            try:
                date_user = input(str('Type the day (DD/MM/YYYY): '))
                date_user = datetime.strptime(date_user, '%d/%m/%Y').date()
            except:
                print('\033[31mPLEASE, INSERT THE DATE CORRECTLY (DD/MM/YYYY)\033[m')
                continue
            else:
                return date_user
