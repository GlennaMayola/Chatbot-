import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PdfChatComponent } from "./components/chat/chat.component";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, PdfChatComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
}
