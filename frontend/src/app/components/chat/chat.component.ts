import { Component } from '@angular/core';
import { PdfChatService } from '../../services/chat.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class PdfChatComponent {
  selectedFile: File | null = null;
  question: string = '';
  answer: string = '';
  isUploading: boolean = false;
  isAsking: boolean = false;

  constructor(private pdfChatService: PdfChatService) {}

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  uploadPDF(): void {
    if (this.selectedFile) {
      this.isUploading = true;
      this.pdfChatService.uploadPDF(this.selectedFile).subscribe({
        next: (res) => {
          alert(res.message);
          this.isUploading = false;
        },
        error: (err) => {
          console.error(err);
          alert('Error uploading PDF');
          this.isUploading = false;
        },
      });
    }
  }

  askQuestion(): void {
    if (this.question.trim()) {
      this.isAsking = true;
      this.pdfChatService.askQuestion(this.question).subscribe({
        next: (res) => {
          this.answer = res.answer || res.error || 'No answer received';
          this.isAsking = false;
        },
        error: (err) => {
          console.error(err);
          this.answer = 'Error getting answer';
          this.isAsking = false;
        },
      });
    }
  }
}
