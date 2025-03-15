package com.cse327project.pitlessbucket.feature_pitlessbucket.data.repository

import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model.FileInfo

interface FileRepository {
    suspend fun getFiles(): Result<List<FileInfo>>
}