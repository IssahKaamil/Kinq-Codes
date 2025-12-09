Module Module1
    Sub Main()
        ' Accepting input for name
        Console.Write("Enter Name: ")
        Dim name As String = Console.ReadLine()

        ' Accepting input for date of birth
        Console.Write("Enter Date of Birth (YYYY-MM-DD): ")
        Dim dob As Date
        If Date.TryParse(Console.ReadLine(), dob) Then
            ' Accepting input for class
            Console.Write("Enter Class: ")
            Dim [class] As String = Console.ReadLine()

            ' Accepting input for age
            Console.Write("Enter Age: ")
            Dim age As Integer
            If Integer.TryParse(Console.ReadLine(), age) Then
                ' Outputting the information
                Console.WriteLine("Name: " & name)
                Console.WriteLine("Date of Birth: " & dob.ToString("yyyy-MM-dd"))
                Console.WriteLine("Class: " & [class])
                Console.WriteLine("Age: " & age)
            Else
                Console.WriteLine("Invalid age input. Please enter a valid integer.")
            End If
        Else
            Console.WriteLine("Invalid date of birth input. Please enter a valid date in YYYY-MM-DD format.")
        End If

        Console.ReadLine() ' To keep the console window open until a key is pressed
    End Sub
End Module
