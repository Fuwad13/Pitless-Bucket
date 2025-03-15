package com.cse327project.pitlessbucket.feature_pitlessbucket.data.repository

import com.cse327project.pitlessbucket.feature_pitlessbucket.data.data_source.api.ApiService
import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model.FileInfo

class FileRepositoryImpl(private val apiService: ApiService) : FileRepository {
    override suspend fun getFiles(): Result<List<FileInfo>> {
        return try {
            val response = apiService.getFiles()
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}