import { Injectable } from '@nestjs/common';
import { firstValueFrom } from 'rxjs';
import { HttpService } from '@nestjs/axios';
import { QueryResponse } from './types/agent-output.types';

@Injectable()
export class AppService {
  constructor(private httpService: HttpService) {}

  getHello(): string {
    return 'Hello World!';
  }

  async executeBuild(prompt: string): Promise<QueryResponse> {
    const agentUrl =
      process.env.AGENT_BACKEND_URL || 'http://localhost:8000';
    const { data } = await firstValueFrom(
      this.httpService.post<QueryResponse>(`${agentUrl}/orchestrate`, {
        query: prompt,
      }),
    );
    return data;
  }
}
