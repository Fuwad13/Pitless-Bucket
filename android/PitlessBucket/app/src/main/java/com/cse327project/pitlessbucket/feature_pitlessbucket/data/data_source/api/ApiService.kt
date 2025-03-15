package com.cse327project.pitlessbucket.feature_pitlessbucket.data.data_source.api

import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model.FileInfo

interface ApiService {
    suspend fun getFiles(): List<FileInfo>
}