#include <iostream>
#include <iomanip>
using namespace std;

// ABSTRACT CLASS
class Person
{
protected:
    char name[50];

public:
    virtual void input() = 0;
    virtual void display() = 0;
};

// STUDENT CLASS
class Student : public Person
{
private:
    int roll;

    char subjects[5][20];
    float marks[5];

    float total;
    float percentage;
    char grade;

public:
    static int count;

    Student()
    {
        total = 0;
        percentage = 0;
        grade = 'F';
        count++;
    }

    void input() override
    {
        cout << "\n===================================";
        cout << "\nEnter Student Details";
        cout << "\n===================================\n";

        cout << "Enter Name: ";
        cin >> name;

        cout << "Enter Roll Number: ";
        cin >> roll;

        if (roll <= 0)
        {
            throw 1;
        }

        cout << "\nEnter 5 Subject Names:\n";

        for (int i = 0; i < 5; i++)
        {
            cout << "Subject " << i + 1 << ": ";
            cin >> subjects[i];
        }

        total = 0;

        cout << "\nEnter Marks:\n";

        for (int i = 0; i < 5; i++)
        {
            cout << subjects[i] << ": ";
            cin >> marks[i];

            if (marks[i] < 0 || marks[i] > 100)
            {
                throw marks[i];
            }

            total += marks[i];
        }

        percentage = total / 5;

        calculateGrade();

        sortSubjects();
    }

    void calculateGrade()
    {
        if (percentage >= 90)
            grade = 'A';

        else if (percentage >= 75)
            grade = 'B';

        else if (percentage >= 60)
            grade = 'C';

        else if (percentage >= 50)
            grade = 'D';

        else
            grade = 'F';
    }

    void display() override
    {
        cout << "\n===================================";
        cout << "\nStudent Report Card";
        cout << "\n===================================\n";

        cout << "Name       : " << name << endl;
        cout << "Roll No.   : " << roll << endl;

        cout << "\nSubjects and Marks\n";
        cout << "-----------------------------------\n";

        for (int i = 0; i < 5; i++)
        {
            cout << setw(15) << left << subjects[i]
                 << " : "
                 << marks[i] << endl;
        }

        cout << "-----------------------------------\n";

        cout << "Total Marks : " << total << "/500" << endl;
        cout << "Percentage  : " << percentage << "%" << endl;
        cout << "Grade       : " << grade << endl;

        cout << "===================================\n";
    }

    bool operator==(int r)
    {
        return roll == r;
    }

    float getPercentage()
    {
        return percentage;
    }

    void swapSubjects(char a[], char b[])
    {
        char temp[20];

        int i;

        for (i = 0; a[i] != '\0'; i++)
        {
            temp[i] = a[i];
        }

        temp[i] = '\0';

        for (i = 0; b[i] != '\0'; i++)
        {
            a[i] = b[i];
        }

        a[i] = '\0';

        for (i = 0; temp[i] != '\0'; i++)
        {
            b[i] = temp[i];
        }

        b[i] = '\0';
    }

    void sortSubjects()
    {
        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < 4 - i; j++)
            {
                if (marks[j] < marks[j + 1])
                {
  
                    float temp = marks[j];
                    marks[j] = marks[j + 1];
                    marks[j + 1] = temp;

                    swapSubjects(subjects[j], subjects[j + 1]);
                }
            }
        }
    }

    static void showCount()
    {
        cout << "\nTotal Students Entered: " << count << endl;
    }

    friend void sortStudents(Student s[], int n);
};

int Student::count = 0;

void sortStudents(Student s[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (s[j].getPercentage() < s[j + 1].getPercentage())
            {
                Student temp = s[j];
                s[j] = s[j + 1];
                s[j + 1] = temp;
            }
        }
    }
}

void searchStudent(Student s[], int n, int key)
{
    bool found = false;

    for (int i = 0; i < n; i++)
    {
        if (s[i] == key)
        {
            cout << "\nStudent Found Successfully!\n";

            s[i].display();

            found = true;

            break;
        }
    }

    if (!found)
    {
        cout << "\nStudent Not Found!\n";
    }
}

int main()
{
    int n;

    cout << "===================================";
    cout << "\n STUDENT MANAGEMENT SYSTEM";
    cout << "\n===================================\n";

    try
    {
        cout << "\nEnter Number of Students: ";
        cin >> n;

        if (n <= 0)
        {
            throw 2;
        }

        Student *s = new Student[n];

        for (int i = 0; i < n; i++)
        {
            try
            {
                cout << "\n\nEntering Details of Student "
                     << i + 1 << endl;

                s[i].input();
            }

            catch (int)
            {
                cout << "\nInvalid Roll Number!\n";
                i--;
            }

            catch (float m)
            {
                cout << "\nInvalid Marks Entered: "
                     << m << endl;

                i--;
            }
        }

        cout << "\n\n===================================";
        cout << "\n ALL STUDENT RECORDS";
        cout << "\n===================================\n";

        for (int i = 0; i < n; i++)
        {
            s[i].display();
        }

        sortStudents(s, n);

        cout << "\n\n===================================";
        cout << "\n STUDENTS SORTED BY PERCENTAGE";
        cout << "\n===================================\n";

        for (int i = 0; i < n; i++)
        {
            s[i].display();
        }

        int key;

        cout << "\nEnter Roll Number to Search: ";
        cin >> key;

        searchStudent(s, n, key);

        Student::showCount();

        delete[] s;
    }

    catch (int)
    {
        cout << "\nInvalid Number of Students!\n";
    }

    cout << "\n\nProgram Finished Successfully!\n";

    return 0;
}