Imports System.IO

Module Module1
    Sub Main()
        ' Specify the file path where you want to save the file
        Dim filePath As String = "C:\Path\To\Your\File.txt"

        ' Sample data to write to the file
        Dim content As String = "Hello, this is the content of the file."

        ' Use StreamWriter to write the content to the file
        Using writer As New StreamWriter(filePath)
            writer.Write(content)
        End Using

        Console.WriteLine("File saved successfully.")
    End Sub
End Module
