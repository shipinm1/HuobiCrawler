using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Data.SQLite;

namespace WindowsFormsApp1
{
   
    public partial class Form1 : Form
    {
        public SQLiteConnection sqlcon;
        public int count = 10;
        
        public Form1()
        {
            InitializeComponent();
        }

        private void refresh_Click(object sender, EventArgs e)
        {
            timer1.Enabled = true;
            timer2.Enabled = true;
            time.Text = count.ToString();
            sqlcon = new SQLiteConnection(@"Data Source=D:\visualApp\huobi\WindowsFormsApp1\huobidata.db;Version=3;");
            sqlcon.Open();
            

            //sql = "CREATE TABLE sell(UID INTEGER PRIMARY KEY, minimum REAL NOT NULL, maximum REAL NOT NULL, price REAL NOT NULL, amount REAL NOT NULL);";
            //SQLiteCommand command = new SQLiteCommand(sql, sqlcon);
            //command.ExecuteNonQuery();
            getSell();
            


            sqlcon.Close();
        }

        public void getSell() {
            string sql = "select * from buy order by price,minimum asc;";

            SQLiteDataAdapter adapter = new SQLiteDataAdapter(sql, sqlcon);
            SQLiteCommandBuilder command = new SQLiteCommandBuilder(adapter);
            DataTable dt = new DataTable();

            adapter.Fill(dt);
            List<string> ls;
            string x;
            string price = "";
            lowsellprice.Text = dt.Rows[0]["price"].ToString();
            foreach (DataRow myRow in dt.Rows)
            {
                ls = new List<string>();
                x = "";
                foreach (DataColumn myColumn in dt.Columns)
                {
                    // Console.Write(myRow[myColumn] + "\t");
                    ls.Add(myRow[myColumn].ToString());
                }
                if (price.CompareTo(ls[3]) == 0)
                {
                    x = string.Format("{0, -10} {1,-10} {2,-10} {3, -10} {4, -10} \n", ls[0], ls[1], ls[2], ls[3], ls[4]);
                    sellBox.Items.Add(x);
                }
                else
                {
                    price = ls[3];
                    sellBox.Items.Add("**********************************************");
                    x = string.Format("{0, -10} {1,-10} {2,-10} {3, -10} {4, -10} \n", ls[0], ls[1], ls[2], ls[3], ls[4]);
                    sellBox.Items.Add(x);
                }

                Console.WriteLine($"{x}");
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            getSell();
            progressBar1.Value = 0;
            count = 10;
            //me.Text = count.ToString();
            MessageBox.Show("fffff");
            
        }

        private void timer2_Tick(object sender, EventArgs e)
        {
            progressBar1.Increment(1);
            time.Text = count.ToString();
            count = count - 1;
            time.Text = count.ToString();
        }



        // 



    }
}
