Attribute VB_Name = "DWPShim"
' DWP Plugin 2.0: semua tombol ribbon memanggil RunAction. Logikanya ada di DWP_Addin.exe (Python), di folder
' DWP_Addin di samping file .ppam. Exe dijalankan tanpa ditunggu, supaya PowerPoint tetap bisa melayani exe.
Option Explicit

Private Const EXE_NAME As String = "DWP_Addin\DWP_Addin.exe"

Public Sub RunAction(control As IRibbonControl)
    Dim exePath As String
    exePath = FindExe()
    If exePath = "" Then
        MsgBox "DWP_Addin.exe tidak ditemukan. Letakkan folder DWP_Addin di samping file DWP_Plugin.ppam.", _
               vbExclamation, "DWP Plugin"
        Exit Sub
    End If
    CreateObject("WScript.Shell").Run """" & exePath & """ " & control.Id, 1, False
End Sub

' Folder add-in yang berisi DWP_Addin\DWP_Addin.exe
Private Function FindExe() As String
    Dim a As AddIn
    For Each a In Application.AddIns
        If a.Path <> "" Then
            If Dir(a.Path & "\" & EXE_NAME) <> "" Then
                FindExe = a.Path & "\" & EXE_NAME
                Exit Function
            End If
        End If
    Next a
End Function
